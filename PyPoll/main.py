# PyPoll
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
poll_csv = os.path.join("Resources","election_data.csv")
poll_output_txt = os.path.join(".", "election_analysis.txt")

# open input file
with open (poll_csv, newline="") as poll_csvfile:
    # make a csv reader for input file
    poll_csvreader = csv.reader(poll_csvfile, delimiter=",")

    # grab header line
    poll_csvheader = next(poll_csvreader)
    
    # store csv columns based on header column text
    voter_index = poll_csvheader.index("Voter ID")
    county_index = poll_csvheader.index("County")
    candidate_index = poll_csvheader.index("Candidate")

    #print(voter_index, county_index, candidate_index)

    # make a dictionary to store candidates
    poll_dict_simple = {}
    poll_dict_complex = {}

    for poll_row in poll_csvreader:
        poll_candidate = poll_row[candidate_index]

        if poll_candidate in poll_dict_simple.keys():
            # candidate in dictionary already, so just increment
            poll_dict_simple[poll_candidate] = poll_dict_simple[poll_candidate] + 1
        else:
            # first instance of candidate, so create key and initialize to 1
            poll_dict_simple[poll_candidate] = 1

    total_votes = 0
    winning_votes = 0
    winner = ""

    for key in poll_dict_simple.keys():
        total_votes += poll_dict_simple[key]
        if poll_dict_simple[key] > winning_votes:
            winning_votes = poll_dict_simple[key]
            winner = key

    for key in poll_dict_simple:
        vote_percentage = (poll_dict_simple[key] / total_votes) * 100
        poll_dict_complex[key] = {"Votes": poll_dict_simple[key], "Percent": vote_percentage, "Winner": key == winner}

    #print(poll_dict_complex)

    output_list = []
    output_list.append("Election Results")
    divider_string = "-" * len(output_list[0]) * 2
    output_list.append(divider_string)
    output_string = f"Total Votes: {total_votes}"
    output_list.append(output_string)
    output_list.append(divider_string)

    for key in poll_dict_complex.keys():
        output_string = f"{key}: {poll_dict_complex[key]['Percent']:.3f}% ({poll_dict_complex[key]['Votes']})"
        output_list.append(output_string)
        if poll_dict_complex[key]["Winner"] == True:
            winner_string = f"Winner: {key}"

    output_list.append(divider_string)
    output_list.append(winner_string)
    output_list.append(divider_string)

    print_stdout(output_list)

    print_file(output_list, poll_output_txt)