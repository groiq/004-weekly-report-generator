#!/usr/bin/env python3

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

# https://github.com/matthewdowney/TogglPy
# ----------------------------------------

    
import json 
from TogglPy import Toggl
toggl = Toggl()

id_path = "data/old-reports-id.txt"
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
pprint(id_vals)


# Date Selection
# --------------

dateStr = "18-06-11"
testdate = datetime.strptime(dateStr, "%y-%m-%d").date()
print(testdate)

day_delta = timedelta(1,0,0)


#backup: date calculation
# start_date = date.today() - (date.weekday(date.today()) * day_delta)
# # print(start_date)
# # ...and go a week back
# start_date = start_date - (day_delta * 7)
# # print(start_date)
# # end date is six days later
# end_date = start_date + (day_delta * 6)
    

    
# out("start date: {}; end date: {}".format(start_date, end_date))
# out("")
# start_date_str = format(start_date)
# end_date_str = format(end_date)

# pprint(start_date_str)
# pprint(end_date_str)

# date =  datetime.strptime(eval.group(1), "%y-%m-%d").date()





















# Uncomment to exit here before accessing toggl's API
# ---------------------------------------------------
exit()






toggl.setAPIKey(id_vals["token"])

# outfile for interim test
# testOutput = open("{}wochenbericht_no_date.txt".format(id_vals["outpath"]),
                # "w", encoding="utf-8")
# def out(item):
    # if item != "":
        # pprint(item,testOutput)
    # else:
        # testOutput.write("\n")


# Retrieve data from toggl API
# ----------------------------



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
# totalTime = timedelta(milliseconds=response["total_grand"])

taskData = response["data"]

# response = json.loads(response)
# print(type(response))

               
# pprint(response)
# out(response)
# for item in response:
    # out(item)
    # out(response[item])
    
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

# out(taskData)
# out("")
taskLog = dict()
timesByProject = dict()
timeFormat = "%Y-%m-%dT%H:%M:%S%z"
# out(taskLog)
# out("")

for item in taskData:
    # out(item)
    projectName = item["project"]
    # out(projectName)
    if projectName in taskLog:
        projectDict = taskLog[projectName]
    else:
        projectDict = dict()
        taskLog[projectName] = projectDict
        timesByProject[projectName] = timedelta(0,0,0)
        # projectDict["totalTime"] = timedelta(0,0,0)

    startTime = datetime.strptime(item["start"], timeFormat)
    # endTime = datetime.strptime(item["end"], timeFormat)
    date = startTime.date()
    if not date in projectDict:
        projectDict[date] = []
    taskEntry = dict()
    projectDict[date].append(taskEntry)
    taskEntry["start"] = startTime.time()
    taskEntry["end"] = datetime.strptime(item["end"],timeFormat).time()
    taskEntry["description"] = item["description"]
    # out(taskEntry["description"])
    taskEntry["duration"] = timedelta(milliseconds = item["dur"])
    timesByProject[projectName] += taskEntry["duration"]
    # for field in taskEntry:
        # out("{}: {}".format(field,taskEntry[field]))
    
    # out(taskLog)
# out(taskLog)
projects = tuple(taskLog.keys())
# out(projects)

# if args.interactive:
    # def projectSelection(projects):
        # returnString = str()
        # for item in projects:
            # returnString += "{} {}\n".format(projects.index(item), item)
        # return returnString
    # print("Select projects to be evaluated. Type the respective numbers:")
    # promptForSelection = input(format(projectSelection(projects)))
    # selectedProjects = []
    # for i in range(len(projects)):
        # if format(i) in promptForSelection:
            # selectedProjects.append(projects[i])
    # print("selected projects:")
    # print(selectedProjects)
# else:
    # selectedProjects = ("Organisation","Programmieren")
selectedProjects = ("Organisation","Programmieren")



# Make a list of daily reports

reports = dict()
for project in selectedProjects:
    for date in taskLog[project]:
        reports[date] = dict()
        # since the dicts aren't filled until later,
        # it doesn't matter if we overwrite one that's already there.

# calculate total time
totalTime = timedelta(0,0,0)
for project in selectedProjects:
    totalTime += timesByProject[project]

# out(totalTime)
# print(totalTime)
# totalTime -= totalTime.days
# out(format(totalTime))
# fullDays = totalTime.days
# totalTime = totalTime.seconds
s = totalTime.seconds
hrs = s // 3600
s = s - (hrs * 3600)
mins = s // 60
hrs = hrs + (totalTime.days * 24)

totalTime = "{} hrs {} mins".format(hrs,mins)

# out(totalTime)
# print(totalTime)
# print("{}h{}min".format(totalTime.hours,totalTime.minutes))
        
# fill daily reports from a manual log file
        
reportFilePath = "{}{}".format(id_vals["outpath"],id_vals["reportFile"])
# print(reportFilePath)
reportSource = open(reportFilePath, "r", encoding="utf-8")

import re

report_regex = r""" 
        \s* bbb \s* 
        2?0?(\d{2}-\d{2}-\d{2}) # Datum
        \s+ (?: - \s+ )?
        (:-[)/(])               # Befindlichkeit
        \s+ (?: - \s+ )?
        ( .+? )                 # Kommentar
        (?: \s* ccc )?
        \s*$
        """
    
for line in reportSource:
    if not "bbb" in line:
        continue
    # out(line)
    # outfile.write(line)
    eval = re.match(report_regex, line, re.X)
    if not eval:
        print("apparent malformed line:")
        print(line)
        continue
    date =  datetime.strptime(eval.group(1), "%y-%m-%d").date()
    if date in reports:
        dateReport = reports[date]
    else:
        continue
    dateReport["smiley"] = eval.group(2)
    dateReport["comment"] = eval.group(3)

reportSource.close()
    
# prompt for missing daily reports

# out(taskLog)

# pprint(reports)

# two ways here:
# i could save the report lines to a list and *only* reopen the reportSource if the list is true.
# Or I could *always* reopen the file and insert lines while working through the reports.
# One means adding an additional list and looping through the report lines a second time.
# The other means an additional file handle even if not needed.
# Unnecessarily opening a file for writing also may be somewhat more risky.
# Another advantage of using an interim list is that I can block the reports added in one run of the generator.

addedReports = []



for date in sorted(reports):
    report = reports[date]
    if not report:
        print("Please write a report for {}:".format(date))
        report = dict()
        report["smiley"] = input("smiley: ")
        while not report["smiley"]:
            report["smiley"] = input("Error: Please enter smiley again. ")
        report["comment"] = input("comment: ")
        while not report["comment"]:
            report["comment"] = input("Error: Please enter comment again. ")
        reports[date] = report
        reportLine = "bbb {} {} {}\n".format(date,report["smiley"],report["comment"])
        # print(reportLine)
        addedReports.append(reportLine)
       
# print(addedReports)
       
if addedReports:
    reportSource = open(reportFilePath, "a", encoding="utf-8")
    reportSource.write("reports added on {}:\n".format(date.today()))
    for reportLine in addedReports:
        reportSource.write(reportLine)

    reportSource.write("\n")
    reportSource.close()
    
# test output
# ------------------

# out("\ntimesByProject")
# out(timesByProject)
# out("")
# out("\ntotalTime")
# out(totalTime)
# out("")
# out("\nreports")
# out(reports)
# out("")
# out("\ntaskLog")
# out(taskLog)
# print(taskLog)
# out(format(totalTime))
# out("")

# Write output
# ------------

outputPath = "{}weekly_report_{}_to_{}.txt".format(id_vals["outpath"],
                                                    start_date,
                                                    end_date)
                                                    
# print(outputPath)
outfile = open(outputPath, "w", encoding="utf-8")
# output = outfile    # I keep writing "output" by mistake

def l():
    outfile.write("\n")

def sep():
    outfile.write("\n{}\n\n".format("=" * 60))
    
sep()
title = "WEEKLY REPORT - {} - {}\n".format(start_date,end_date)
outfile.write(title)
# l()
# outfile.write("=" * len(title))
# l()
outfile.write("Total time: ")
outfile.write(format(totalTime))

l()

# outfile.write("Total time: {}\n".format(totalTime))
sep()
fieldOrder = ("description","start","end","duration")
# print task fields in right order. (Why does this work out-of-the-box)
# in version 3?

for date in sorted(reports):
    
    # outfile.write(date)
    outfile.write("{}\n\n".format(date.strftime("%a %d. %m. %y")))
    outfile.write("smiley: {}\n".format(reports[date]["smiley"]))
    outfile.write("comment: {}\n".format(reports[date]["comment"]))
    
    # for item in reports[date]:
        # outfile.write("{}: {}\n".format(item,reports[date][item]))
    outfile.write("\nTasks:\n")
    dailyTime = timedelta(0,0,0)
    
    for project in taskLog:
        if not date in taskLog[project]:
            continue
        for task in taskLog[project][date]:
            
            outfile.write("---\n")
            outfile.write("project: {}\n".format(project))
            # outfile.write("description: {}\n".format(task[description]))
            dailyTime += task["duration"]
            
            for field in fieldOrder:
                outfile.write("{}: {}\n".format(field, task[field]))
            
            # outfile.write(format(task))
        outfile.write("\nTotal time: {}\n".format(dailyTime))

    
    sep()





outfile.close()









# NEXT - sanitize data: reports should be stored outside of the main dict
# THEN - make a dict for total times by project


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
