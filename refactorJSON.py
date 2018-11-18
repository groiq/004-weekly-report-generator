#!/usr/bin/env python3

# Rewrite a JSON whose outermost layer is an array. The last entry in the array
#  is a summary of the data in the previous entries. I want to make a dict as
#  outer layer with an entry "summary" containing the last entry and an entry
#  "data" containing the original array minus the summary.

import json
from pprint import pprint

filePath = "./data/compareWeeksJson.txt"

# read data from file
# -------------------
#json = json.load(open(filePath,"r",encoding="utf-8"))
intext = open(filePath,"r",encoding="utf-8").read()

#incoming = json.loads(open('./data/compareWeeksJson.txt').read())
#pprint(intext)
parsed = json.loads(intext)
#print(incoming[-1])

# Issue is that json parser can't handle single quotes. Also, cannot handle
#  datetime because not a standard variable type.
