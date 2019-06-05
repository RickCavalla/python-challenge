# PyBank
import os
import csv

# function to output list to terminal
# one list item per line
def print_stdout(pList):
    for list_item in pList:
        print(list_item)

# function to output list to a file
# one list item per line
def print_file(pList, pFilename):
    with open(pFilename, "w") as textwriter:
        for list_item in pList:
            textwriter.write(list_item)
            textwriter.write("\n")

# define path to input data
bank_csv = os.path.join("Resources","budget_data.csv")
bank_output_txt = os.path.join(".", "bank_analysis.txt")

# open input file
with open (bank_csv, newline="") as bank_csvfile:
    # make a csv reader for input file
    bank_csvreader = csv.reader(bank_csvfile, delimiter=",")

    # grab header line
    bank_csvheader = next(bank_csvreader)
    
    # store csv columns based on header column text
    date_index = bank_csvheader.index("Date")
    profit_index = bank_csvheader.index("Profit/Losses")

    # initialize variables
    bank_months = 0
    net_profit = 0
    this_profit = 0    
    profit_delta = 0
    total_profit_delta = 0
    average_profit_delta = 0
    profit_max = 0
    profit_max_date = ""
    loss_max = 0
    loss_max_date = ""

    # prior profit is undefined at start, not zero
    # had to google how to do null values in Python
    last_profit = None

    # loop through data rows
    for bank_row in bank_csvreader:
        # increment counter for months of data
        bank_months += 1

        # grab profit/loss on this road as a decimal
        this_profit = float(bank_row[profit_index])

        # grab difference in profit compared to last month,
        # unless prior month undefined
        if last_profit is None:            
            profit_delta = 0
        else:
            profit_delta = this_profit - last_profit

        # check for new max profit
        if profit_delta > profit_max:
            profit_max = profit_delta
            profit_max_date = bank_row[date_index]

        # check for new max loss
        if profit_delta < loss_max:
            loss_max = profit_delta
            loss_max_date = bank_row[date_index]

        # aggregate profit diff
        total_profit_delta += profit_delta

        # aggregate total profits
        net_profit += this_profit

        # store row profit in temporary variable,
        # so available for compare to next month
        last_profit = this_profit

    # average profit swing is sum of profit swings, divided by swings
    # no swing defined for first month, 
    # thus total profit swings are one less than total months
    average_profit_delta = total_profit_delta / (bank_months - 1)

    # put nicely formatted output in a list since we have to output twice.
    # with output in list, don't have to write this code twice 
    output_list = []
    output_list.append("Financial Analysis")
    output_list.append("------------------")
    output_list.append(f"Total Months: {bank_months}")
    output_list.append(f"Total: ${net_profit:.2f}")
    output_list.append(f"Average Change: ${average_profit_delta:.2f}")
    output_list.append(f"Greatest Increase in Profits: {profit_max_date} ${profit_max:.2f}")
    output_list.append(f"Greatest Decrease in Profits: {loss_max_date} ${loss_max:.2f}")

    # function call - output to terminal
    print_stdout(output_list)

    # function call - output to a file
    print_file(output_list, bank_output_txt)
