#!/usr/bin/ env python3

# Imports
# -------

output = list()
errlog = list()

from argparse import ArgumentParser
# import datetime
from datetime import date,datetime,timedelta

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

# Set up a list of entries for the selected days
# ----------------------------------------------

listOfDays = []

date = start_date
while date <= end_date:
    print(date)
    dayEntry = dict()
    dayEntry["date"] = date
    dayEntry["report"] = dict()
    dayEntry["tasks"] = []
    dayEntry["total time"] = timedelta(0,0,0)
    listOfDays.append(dayEntry)
    date += day_delta

# print(listOfDays)
for day in listOfDays:
    print(day)

# Then have the program retrieve data.
# Then set up project selection from the retrieved data.

# If there's no report, prompt for one.






# Write output
# ------------

if errlog:
    outfile = open("errlog.txt", "w", encoding="utf-8")
    for entry in errlog:
        try:
            outfile.write(entry)
        except:
            outfile.write(format(entry))
        outfile.write("\n")
    outfile.close()
    
# The actual outfile will be formatted using the dates evaluated.
# All this later.

# Final readln
# ------------

readln = input("Press enter to exit program.")
