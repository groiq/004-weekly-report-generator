#!/usr/bin/env python3

# This will retrieve summary reports from the toggl API for consecutive weeks
# and store the logged times by project for further comparisons.

# Imports
# -------

from pprint import pprint
from datetime import date,datetime,timedelta

