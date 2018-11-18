#!/usr/bin/env python3

# Rewrite a JSON whose outermost layer is an array. The last entry in the array
#  is a summary of the data in the previous entries. I want to make a dict as
#  outer layer with an entry "summary" containing the last entry and an entry
#  "data" containing the original array minus the summary.

