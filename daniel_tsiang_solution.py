"""
Developer's name: Daniel Tsiang
"""
from datetime import datetime as dt
import pandas as pd

# param hour: int
def convert_hour_to_key(hour):
    return (str(hour) + ':00') if (hour > 9) else ('0' + str(hour) + ':00')

def process_shifts(path_to_csv):
    """

    :param path_to_csv: The path to the work_shift.csv
    :type string:
    :return: A dictionary with time as key (string) with format %H:%M
        (e.g. "18:00") and cost as value (Number)
    For example, it should be something like :
    {
        "17:00": 50,
        "22:00: 40,
    }
    In other words, for the hour beginning at 17:00, labour cost was
    50 pounds
    :rtype dict:
    """
    # Read csv file
    df = pd.read_csv(path_to_csv)

    # Remove white spaces and AM/PM from columns
    df['break_notes'] = df['break_notes'].str.replace(' ', '')
    df['break_notes'] = df['break_notes'].str.replace('PM', '')
    df['break_notes'] = df['break_notes'].str.replace('AM', '')
    df['break_notes'] = df['break_notes'].str.replace('.', ':')

    # Split break_notes column into two separate columns using '-'
    df[['start_break','end_break']] = df.break_notes.str.split("-", n = 1, expand = True)

    # Dropping old columns
    df.drop(columns =["break_notes"], inplace = True)

    # Convert break times to 24-hour format
    mylist = ['.', ':']
    minutes = ':00'
    for index, row in df.iterrows():
        if all(x not in row['start_break'] for x in mylist):
            df.loc[index, 'start_break'] += minutes
        if all(x not in row['end_break'] for x in mylist):
            df.loc[index, 'end_break'] += minutes
        # Convert times to datetime values
        df.loc[index,'end_time'] = dt.strptime(df.loc[index, 'end_time'], "%H:%M")
        df.loc[index,'start_time'] = dt.strptime(df.loc[index, 'start_time'], "%H:%M")
        df.loc[index,'start_break'] = dt.strptime(df.loc[index, 'start_break'], "%H:%M")
        df.loc[index,'end_break'] = dt.strptime(df.loc[index, 'end_break'], "%H:%M")
        # Correct break time to PM time if necessary
        if df.loc[index,'start_break'] < df.loc[index,'start_time'] and \
        df.loc[index,'start_time'] < df.loc[index, 'end_time']:
            df.loc[index, 'start_break'] += pd.Timedelta(hours=12)
            df.loc[index, 'end_break'] += pd.Timedelta(hours=12)

    # Initialise shifts dictionary with hourly times and 0 labour costs
    shifts = {}
    for i in range(24):
        hour = convert_hour_to_key(i)
        shifts.update({hour : 0})

    # Calculate labour cost per hour
    for index, row in df.iterrows():
        start_shift_hour = row['start_time'].hour
        end_shift_hour = row['end_time'].hour
        # This accounts for if shift starts at PM but finishes at AM
        if end_shift_hour < start_shift_hour:
            end_shift_hour += 24
        for hour_index in range(start_shift_hour, end_shift_hour + 1):
            hour = hour_index - 24 if hour_index >= 24 else hour_index
            key = convert_hour_to_key(hour)
            pay = 0
            # Check if hour is in break time
            if hour >= row['start_break'].hour and hour <= row['end_break'].hour:
                if hour < row['end_break'].hour:
                    # Skip this hour, no pay as break hour
                    continue
                # Enter here if break time less than 1 hour
                break_time_in_hours = pd.Timedelta(df.loc[index,'end_break'] - dt.strptime(key, '%H:%M')).seconds / 3600
                pay = (1 - break_time_in_hours) * row['pay_rate']
            else:
                # This if statement accounts for if last hour worked is less than 1 hour
                if hour == end_shift_hour:
                    work_time_in_hours = pd.Timedelta(df.loc[index,'end_time'] - dt.strptime(key, '%H:%M')).seconds / 3600
                    pay = work_time_in_hours * row['pay_rate']
                else:
                    pay = row['pay_rate']
            # Converts key to correct value to be stored in shifts dictionary
            if hour >= 24:
                shifts[convert_hour_to_key(hour-24)] += pay
            else:
                shifts[key] += pay

    return shifts


def process_sales(path_to_csv):
    """

    :param path_to_csv: The path to the transactions.csv
    :type string:
    :return: A dictionary with time (string) with format %H:%M as key and
    sales as value (string),
    and corresponding value with format %H:%M (e.g. "18:00"),
    and type float)
    For example, it should be something like :
    {
        "17:00": 250,
        "22:00": 0,
    },
    This means, for the hour beginning at 17:00, the sales were 250 dollars
    and for the hour beginning at 22:00, the sales were 0.

    :rtype dict:
    """
    # Define date parser lambda function
    d_parser = lambda x: dt.strptime(x, '%H:%M')

    # Parse dates while reading csv file
    df1 = pd.read_csv('transactions.csv', parse_dates=['time'], date_parser=d_parser)

    # Resample csv data on hourly basis and sum amounts in each hour
    df = df1.resample('60min', on='time').sum()

    # Initialise sales dictionary with hourly times and 0 sales
    sales = {}
    for i in range(24):
        hour = convert_hour_to_key(i)
        sales.update({hour : 0})

    # Iterate through rows and add sales amount for each hour
    for time, row in df.iterrows():
        hours = time.hour
        hour = convert_hour_to_key(hours)
        amount = round(row['amount'], 2)
        sales.update({hour : amount})

    return sales

def compute_percentage(shifts, sales):
    """

    :param shifts:
    :type shifts: dict
    :param sales:
    :type sales: dict
    :return: A dictionary with time as key (string) with format %H:%M and
    percentage of labour cost per sales as value (float),
    If the sales are null, then return -cost instead of percentage
    For example, it should be something like :
    {
        "17:00": 20,
        "22:00": -40,
    }
    :rtype: dict
    """
    # Initialise empty percentages dictionary
    percentages = {}

    # Iterate through each hour and calculate percentages
    for (hour1, sale), (hour2, labour) in zip(sales.items(), shifts.items()):
        if sale > 0:
            percentage = (labour/sale) * 100
        else:
            percentage = -1 * labour if labour > 0 else 0
        percentages.update({hour1 : percentage})

    return percentages

def best_and_worst_hour(percentages):
    """

    Args:
    percentages: output of compute_percentage
    Return: list of strings, the first element should be the best hour,
    the second (and last) element should be the worst hour. Hour are
    represented by string with format %H:%M
    e.g. ["18:00", "20:00"]

    """
    # worst_hour is the key of the most negative percentage, or maximum percentage if no negative percentages
     # min_key is the key whose value is the smallest
    min_key = min(percentages, key=percentages.get)
    if (percentages[min_key] < 0):
        worst_hour = min_key
    else:
        worst_hour = max(percentages, key=percentages.get)

    # best_hour is the key of the minimum positive percentage
    best_hour = min(
        (percentage, hour)
        for (hour, percentage) in percentages.items()
        if percentage > 0
    )[1]


    print(f"best hour: {best_hour}, worst hour: {worst_hour}")

    return [best_hour, worst_hour]

def main(path_to_shifts, path_to_sales):
    """
    Do not touch this function, but you can look at it, to have an idea of
    how your data should interact with each other
    """

    shifts_processed = process_shifts(path_to_shifts)
    sales_processed = process_sales(path_to_sales)
    percentages = compute_percentage(shifts_processed, sales_processed)
    best_hour, worst_hour = best_and_worst_hour(percentages)
    return best_hour, worst_hour

if __name__ == '__main__':
    # You can change this to test your code, it will not be used
    path_to_sales = "transactions.csv"
    path_to_shifts = "work_shifts.csv"
    best_hour, worst_hour = main(path_to_shifts, path_to_sales)


# Developer's name: Daniel Tsiang
