#!/usr/bin/env python3

# This will retrieve summary reports from the toggl API for consecutive weeks
# and store the logged times by project for further comparisons.

# Imports
# -------

from pprint import pprint
from datetime import date,datetime,timedelta

# Variables
# ---------

firstMonday = date(2017,8,28)
firstSunday = date(2017,9,3)

tag = timedelta(1,0,0)

curMonday = firstMonday
curSunday = firstSunday

testOutput = [{'mon': '12766-03-1', 'sun': '12766-03-7', 'times': {'coding': '15:00:00', 'writing': '15:00:00', 'reading': '15:00:00', 'gaming': '15:00:00'}}, {'mon': '12766-03-8', 'sun': '12766-03-14', 'times': {'coding': '15:00:00', 'writing': '15:00:00', 'reading': '15:00:00', 'gaming': '15:00:00'}}, {'mon': '12766-03-15', 'sun': '12766-03-21', 'times': {'coding': '15:00:00', 'writing': '15:00:00', 'reading': '15:00:00', 'gaming': '15:00:00'}}, {'mon': '12766-03-22', 'sun': '12766-03-28', 'times': {'coding': '15:00:00', 'writing': '15:00:00', 'reading': '15:00:00', 'gaming': '15:00:00'}}]

datalog = []







with open("./data/compareWeeksJson.txt","w",encoding="utf-8") as outfile:
    pprint(testOutput,outfile)
    
    pprint(datalog,outfile)

