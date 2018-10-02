#!/usr/bin/env python3

# auto-write report lines for a range of dates.
# thanks to https://stackoverflow.com/questions/1060279/iterating-through-a-range-of-dates-in-python

import datetime

start_date = datetime.date(2018,6,11)
end_date = datetime.date(2018,9,3)

d = start_date
delta = datetime.timedelta(days=1)
while d <= end_date:
    print(d.strftime("%Y-%m-%d"))
    d += delta