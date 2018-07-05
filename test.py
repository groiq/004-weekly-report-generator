#!/usr/bin/env python3

from datetime import datetime

timestring = '2018-07-01T21:30:04+02:00'

timeFormat = "%Y-%m-%dT%H:%M:%S%z"


timestring = "2018-07-01T21:30:04+02:00"
timeFormat = "%Y-%m-%dT%H:%M:%S%z"



time = datetime.strptime(timestring, timeFormat)

print(time)