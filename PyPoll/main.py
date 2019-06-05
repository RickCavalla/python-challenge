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

# define path to results file 
poll_output_txt = os.path.join(".", "election_analysis.txt")

# open input file
with open (poll_csv, newline="") as poll_csvfile:
    # make a csv reader for input file
    poll_csvreader = csv.reader(poll_csvfile, delimiter=",")

    # grab header line
    poll_csvheader = next(poll_csvreader)
    
    # store csv columns based on header column text.
    # if we move around or add columns, column numbers could change,
    # but column header should be constant
    voter_index = poll_csvheader.index("Voter ID")
    county_index = poll_csvheader.index("County")
    candidate_index = poll_csvheader.index("Candidate")

    # make a simple dictionary to store candidate votes while reading file
    poll_dict_simple = {}

    # make a more complex dictionary to store expanded candidate info
    # this will be populated at end, after we know all the data
    poll_dict_complex = {}

    # loop through input data rows
    for poll_row in poll_csvreader:
        # pull name of candidate that received vote
        poll_candidate = poll_row[candidate_index]

        # check if candidate in simple dictionary
        if poll_candidate in poll_dict_simple.keys():
            # candidate in dictionary already, so just increment vote value
            poll_dict_simple[poll_candidate] = poll_dict_simple[poll_candidate] + 1
        else:
            # first instance of candidate, so create key and initialize votes to 1
            poll_dict_simple[poll_candidate] = 1

    total_votes = 0
    most_votes = 0
    winner = ""

    # loop through simple dictionary,
    # summing up total votes and figuring out who had most votes
    for candidate_key in poll_dict_simple.keys():
        total_votes += poll_dict_simple[candidate_key]

        # if more votes than any prior candidate, treat as winner for now.
        # can be overwritten in future iteration if we find someone with more votes
        if poll_dict_simple[candidate_key] > most_votes:
            most_votes = poll_dict_simple[candidate_key]
            winner = candidate_key

    # loop through simple dictionary and create a new dictionary.
    # key is still candidate, but now multiple named items linked to candidate,
    # so it is a dictionary that contains a dictionary
    for candidate_key in poll_dict_simple:
        vote_percentage = (poll_dict_simple[candidate_key] / total_votes) * 100
        poll_dict_complex[candidate_key] = {
            "Votes": poll_dict_simple[candidate_key],
            "Percent": vote_percentage,
            "Winner": candidate_key == winner
            }

    # put nicely formatted output in a list since we have to output twice.
    # with output in list, don't have to write this code twice. 
    output_list = []
    output_list.append("Election Results")

    # make divider line that is twice length of first output line.
    # can append this to list multiple times and all will line up.
    # no need to worry about typing out dashes by hand each time
    divider_string = "-" * len(output_list[0]) * 2
    output_list.append(divider_string)

    output_string = f"Total Votes: {total_votes}"
    output_list.append(output_string)
    output_list.append(divider_string)

    # loop through complex dict and format a line with each candidate data
    for candidate_key in poll_dict_complex.keys():
        # create output line for this candidate
        output_string = (
            f"{candidate_key}:"
            + f" {poll_dict_complex[candidate_key]['Percent']:.3f}%"
            + f" ({poll_dict_complex[candidate_key]['Votes']})"
            )
        output_list.append(output_string)

        # if Winner key has value of true, create a string stating that.
        # do not output yet
        if poll_dict_complex[candidate_key]["Winner"] == True:
            winner_string = f"Winner: {candidate_key}"

    output_list.append(divider_string)

    # output winner string now that all candidate data displayed
    output_list.append(winner_string)

    output_list.append(divider_string)

    # function call - output to terminal
    print_stdout(output_list)

    # function call - output to a file
    print_file(output_list, poll_output_txt)