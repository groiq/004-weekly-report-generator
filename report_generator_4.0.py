#!/usr/bin/ env python3

# Imports
# -------

from pprint import pprint
from argparse import ArgumentParser
# import datetime
from datetime import date,datetime,timedelta

output = list()
errlog = list()

# Parameters
# ----------

parser = ArgumentParser(fromfile_prefix_chars='@', 
                        description="read a timelog and generate a report")
parser.add_argument("-i", "--interactive", action="store_true", 
                    help="interactive mode")
parser.add_argument("-m", "--mail", action="store_true",
                    help="send report via email")
                    
args = parser.parse_args()

# Date Selection
# --------------

day_delta = timedelta(1,0,0)

# Methods for prompting for dates. These are repeated if there are issues
# with the input.
def dateInput():
    date_year = datePartInput("year")
    if date_year < 100:
        date_year += 2000
    date_month = datePartInput("month")
    date_day = datePartInput("day")
    try:
        result = date(date_year,date_month,date_day)
    except:
        print("Something went wrong with building the date. Retry.")
        result = dateInput()
    return result
    
def datePartInput(prompt: str):
    result = input("{} : ".format(prompt))
    if result:
        try:
            result = int(result)
        except:
            print("Couldn't parse input. Please retry.")
            result = datePartInput(prompt)
    else:
        print("Input empty. Defaulting to current {}.".format(prompt))
        # TTT set value to current
    return result
    
if args.interactive:
    print("Select evaluated time range by giving the first and last day.")
    print("Leave lines blank for current year/month.")
    print("first date:")
    start_date = dateInput()
    print("last date:")
    end_date = dateInput()
else:
    # set start_date to this monday...
    start_date = date.today() - (date.weekday(date.today()) * day_delta)
    # ...and go a week back
    start_date = start_date - (day_delta * 7)
    # end date is six days later
    end_date = start_date + (day_delta * 6)

print("start date: {}\nend date: {}".format(start_date, end_date))

start_date_str = format(start_date)
end_date_str = format(end_date)

pprint(start_date_str)
pprint(end_date_str)

# Set up a list of entries for the selected days
# ----------------------------------------------

listOfDays = []

date = start_date
while date <= end_date:
    # print(date)
    dayEntry = {}
    dayEntry["date"] = date
    dayEntry["report"] = dict()
    dayEntry["tasks"] = []
    dayEntry["total time"] = timedelta(0,0,0)
    listOfDays.append(dayEntry)
    date += day_delta

# pprint(listOfDays)

# Retrieve data from toggl API
# ----------------------------

# https://github.com/matthewdowney/TogglPy
    
import json 
from TogglPy import Toggl
toggl = Toggl()

id_path = "data/id.txt"
id_vals = {}

id_file = open(id_path, "r", encoding="utf-8")
id_path = id_file.readline().strip()
print(id_path)
id_file = open(id_path, "r", encoding="utf-8")
for line in id_file:
    line = line.strip().split("::")
    id_key = line[0]
    id_val = line[1]
    id_vals[id_key] = id_val
# pprint(id_vals)

toggl.setAPIKey(id_vals["token"])



# for workspace in toggl.getWorkspaces():
    # print("Workspace: {}; id: {}".format(workspace["name"],workspace["id"]))

request_params = {
                "workspace_id": id_vals["id"],
                "user_agent": id_vals["uagent"],
                "since": start_date_str,
                "until": end_date_str,
                }
    
response = toggl.request("https://toggl.com/reports/api/v2/details", 
            parameters=request_params)

# pprint(response)

for item in response:
    output.append(item)
    output.append(response[item])
    
# Then have the program retrieve data.
# Then set up project selection from the retrieved data.

# If there's no report, prompt for one.

# Move the "set up list of entries" code down past the retrieve part






# Write output
# ------------

if errlog:
    errfile = open("{}errlog.txt".format(id_vals["outpath"]), "w", 
                    encoding="utf-8")
    for entry in errlog:
        try:
            errfile.write(entry)
        except:
            errfile.write(format(entry))
        errfile.write("\n")
    errfile.close()

outfile = open("{}wochenbericht_no_date.txt".format(id_vals["outpath"]),
                "w", encoding="utf-8")
# outfile.write(format(response))
for item in output:
    outfile.write(format(item))
    # try:
        # outfile.write(item)
    # except:
        # outfile.write(format(item))
    outfile.write("\n")
outfile.close()

# The actual outfile will be formatted using the dates evaluated.
# All this later.

# Final readln
# ------------

readln = input("Press enter to exit program.")
