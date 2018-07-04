#!/usr/bin/ env python3

from datetime import date,datetime,timedelta

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

print("Select evaluated time range by giving the first and last day.")
print("Leave lines blank for current year/month.")
print("first date:")
testdate = dateInput()
  

print(testdate)