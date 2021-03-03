# CSV metrics

### Description
Python code to understand the most and least profitable hour of the day for a given restaurant when considering labour cost and gross sales. Data is parsed from two CSVs, one describing the shifts, and the other one describing the hourly sales revenue.

### Example
![Output from code](https://user-images.githubusercontent.com/74436899/109802876-3ed2e500-7c18-11eb-8fcd-0669a67a52b7.png "Output from code")

#### Labour Data
A shift will include the pay-rate (per hour), the start and end time, and a text field where the manager will enter break info. This may vary depending on the individual manager.

For example:
```
{
    'break_notes': '15-18',
    'start_time': '10:00',
    'end_time': '23:00',
    'pay_rate': 10.0
}
```

The data given shows a shift started at 10AM and ended at 11PM. However, the break_notes "15-18" indicates that the staff member took a 3 hour break in the middle of the day (when they would not be paid). The employee was paid £10 per hour.

#### Sales Data
This shows you a set of transactions:

For example
```
{
    'time' : '10:31,
    'amount' : 50.32
}
```

This code can compute different metrics for the different hours,
such as the total sales during this hour, the cost of labour for this hour, and
the cost of labour as percentage of sales.

e.g.,
```
Hour  Sales	  Labour     %
7:00	100	    30	    30%
8:00	300	    60	    20%
```

#### Best and Worst Hours
Lastly, the code can output which hour was the best and worst in terms of labour cost as a percentage of sales. If the sales are null, then -cost is returned instead of percentage. (e.g -40).

### Technologies Used
* Python

### Goals
* Refresh skills in Python and Pandas library.
* Utilise Python to parse and clean data from csv files.
* Be able to handle time period data entered in different formats.
* Resample datetime and financial data into hourly basis, and store in dictionaries data structure.
* Calculate most and least profitable hour based on revenue from sales and labour cost.

### Getting Started
1. With transaction.csv and work_shifts.csv in the same folder, in the terminal, run "python daniel_tsiang_solution.py".
2. The best and worst hours for the restaurant will be printed to the terminal.

### Contribution Guidelines
If you would like to contribute code, identify bugs, or propose improvements, please fork this repository and submit a pull request with your suggestions. Below are some helpful links to help you get started:
1. [Project's main repository](https://github.com/DanielTsiang/CSV-metrics-Python)
2. [Project's issue tracker](https://github.com/DanielTsiang/CSV-metrics-Python/issues)
