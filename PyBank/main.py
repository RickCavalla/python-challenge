# PyBank
import os
import csv

bank_csv = os.path.join("Resources","budget_data.csv")

with open (bank_csv, newline="") as bank_csvfile:
    bank_csvreader = csv.reader(bank_csvfile, delimiter=",")

    bank_csvheader = next(bank_csvreader)
    
    date_index = bank_csvheader.index("Date")
    profit_index = bank_csvheader.index("Profit/Losses")

    bank_months = 0
    net_profit = 0
    this_profit = 0
    last_profit = None
    profit_delta = 0
    total_profit_delta = 0
    average_profit_delta = 0
    profit_max = 0
    profit_max_date = ""
    loss_max = 0
    loss_max_date = ""

    for bank_row in bank_csvreader:
        bank_months += 1

        this_profit = float(bank_row[profit_index])

        if last_profit is None:            
            # nothing to compare
            profit_delta = 0
        else:
            profit_delta = this_profit - last_profit

        if profit_delta > profit_max:
            profit_max = profit_delta
            profit_max_date = bank_row[date_index]

        if profit_delta < loss_max:
            loss_max = profit_delta
            loss_max_date = bank_row[date_index]

        total_profit_delta += profit_delta

        net_profit += this_profit

        last_profit = this_profit

    average_profit_delta = total_profit_delta / (bank_months - 1)

    output_list = []
    output_list.append("Financial Analysis")
    output_list.append("------------------")
    output_list.append(f"Total Months: {bank_months}")
    output_list.append(f"Total: ${net_profit:.2f}")
    output_list.append(f"Average Change: ${average_profit_delta:.2f}")
    output_list.append(f"Greatest Increase in Profits: {profit_max_date} ${profit_max:.2f}")
    output_list.append(f"Greatest Decrease in Profits: {loss_max_date} ${loss_max:.2f}")
    
    print(*output_list, sep="\n")
