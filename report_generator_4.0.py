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
    result = date.today()
    components = { "year": result.year, "month": result.month, 
                    "day": result.day }
    for component in components:
        components[component] = datePartInput(component,components)
    if components["year"] < 100:
        components["year"] += 2000
    try:
        result = date(components["year"], components["month"], 
                    components["day"])
    except:
        print(components)
        print("Something went wrong with building the date. Retry.")
        result = dateInput()
    return result
    
def datePartInput(prompt: str,components: dict):
    result = input("{} : ".format(prompt))
    if result:
        try:
            result = int(result)
        except:
            print("Couldn't parse input. Please retry.")
            result = datePartInput(prompt)
    else:
        print("Input empty. Defaulting to current {}.".format(prompt))
        result = components[prompt]
    return result
    
if args.interactive:
    print("Select evaluated time range by giving the first and last day.")
    print("Leave lines blank for current year/month.")
    print("first date:")
    start_date = dateInput()
    print("last date:")
    end_date = dateInput()
    if end_date < start_date:
        print("End date before start date. Swapping values.")
        dummy_date = start_date
        start_date = end_date
        end_date = dummy_date
else:
    # set start_date to this monday...
    start_date = date.today() - (date.weekday(date.today()) * day_delta)
    # ...and go a week back
    start_date = start_date - (day_delta * 7)
    # end date is six days later
    end_date = start_date + (day_delta * 6)

output.append("start date: {}; end date: {}".format(start_date, end_date))
output.append("")
start_date_str = format(start_date)
end_date_str = format(end_date)

# pprint(start_date_str)
# pprint(end_date_str)


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
# print(id_path)
id_file = open(id_path, "r", encoding="utf-8")
for line in id_file:
    line = line.strip().split("::")
    id_key = line[0]
    id_val = line[1]
    id_vals[id_key] = id_val
# pprint(id_vals)

toggl.setAPIKey(id_vals["token"])

# outfile for interim test
outfile = open("{}wochenbericht_no_date.txt".format(id_vals["outpath"]),
                "w", encoding="utf-8")
def out(item):
    pprint(item,outfile)


# for workspace in toggl.getWorkspaces():
    # print("Workspace: {}; id: {}".format(workspace["name"],workspace["id"]))

request_params = {
                "workspace_id": id_vals["id"],
                "user_agent": id_vals["uagent"],
                "since": start_date_str,
                "until": end_date_str,
                }
    
# fetch data via API call
response = toggl.request("https://toggl.com/reports/api/v2/details", 
            parameters=request_params)

# temporary: read data from local file
# infile = open("{}wochenbericht_temp_input.txt".format(id_vals["outpath"]), 
                # "r", encoding="utf-8")
# response = infile.read()
# infile.close()

# Extract data
# ------------

# totalTime = response["total_grand"]
totalTime = timedelta(milliseconds=response["total_grand"])

taskData = response["data"]

# response = json.loads(response)
# print(type(response))

               
# pprint(response)
# output.append(response)
# for item in response:
    # output.append(item)
    # output.append(response[item])
    
# Transfer the data to a format I can work with
# ---------------------------------------------

# Okay, so the steps are:
# - get a list of projects
# - prompt for project selection
# - work through the entries
#   - if entry project is selected, evaluate
#   - add entry to data for the day

# So for now, I'll sort the entries first by project, then by date.

# Apart from the dates, one dict entry is reserved for the report.

# Later: do the same with a database!

taskLog = dict()
timeFormat = "%Y-%m-%dT%H:%M:%S%z"
output.append(taskLog)
output.append("")

for item in taskData:
    output.append(item)
    project = item["project"]
    taskLog[project] = {}
    startTime = datetime.strptime(item["start"], timeFormat)
    endTime = datetime.strptime(item["end"], timeFormat)
    date = startTime.date()
    taskLog[project][date] = []
    output.append("--------------------")
    output.append(taskLog)
    output.append("")
    # output.append("start time")
    # output.append(startTime)
    # output.append(format(startTime))
    # print(item["start"])
    # print(type(item["start"]))
    # output.append(item)

# output.append(taskLog)
    
# listOfDays = []

# date = start_date
# while date <= end_date:
    # # print(date)
    # dayEntry = {}
    # dayEntry["date"] = date
    # dayEntry["report"] = dict()
    # dayEntry["tasks"] = []
    # dayEntry["total time"] = timedelta(0,0,0)
    # listOfDays.append(dayEntry)
    # date += day_delta

# pprint(listOfDays)
 

# First, set up a dict of the entire task list.
 
 
# Then set up project selection from the retrieved data.

# If there's no report, prompt for one.

# Move the "set up list of entries" code down past the retrieve part




# add data to output
# ------------------

output.append(format(totalTime))
output.append("")

for item in taskData:
    output.append(item)


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

# outfile = open("{}wochenbericht_no_date.txt".format(id_vals["outpath"]),
                # "w", encoding="utf-8")
# outfile.write(format(response))
# for item in output:
    # pprint(item,outfile)
    # if not item:
        # outfile.write("\n")
    # # outfile.write(format(item))
    # # try:
        # # outfile.write(item)
    # # except:
        # # outfile.write(format(item))
    # # outfile.write("\n")
# outfile.close()

# The actual outfile will be formatted using the dates evaluated.
# All this later.

# Final readln
# ------------

readln = input("Press enter to exit program.")
