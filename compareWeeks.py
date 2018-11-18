#!/usr/bin/env python3

# This will retrieve summary reports from the toggl API for consecutive weeks
# and store the logged times by project for further comparisons.

# Imports
# -------

from pprint import pprint
from datetime import date,datetime,timedelta

# Variables
# ---------

firstMonday = datetime.date(2017,8,28)
firstSunday = datetime.date(2017,9,3)

tag = datetime.timedelta(1,0,0)

curMonday = firstMonday
curSunday = firstSunday

