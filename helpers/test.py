#!/usr/bin/env python3

from pprint import pprint

outfile = open("test-output.txt", "w", encoding="utf-8")

def out(item="\n"):
    if item != "\n":
        pprint(item,outfile)
    else:
        outfile.write("\n")

oldSort = {'classroom': {'mon': ['cm0', 'cm1'],
               'tue': ['ct0', 'ct1'],
               'wed': ['cw0', 'cw1']},
 'desk': {'mon': ['dm0', 'dm1'], 'tue': ['dt0', 'dt1'], 'wed': ['dw0', 'dw1']},
 'library': {'mon': ['lm0', 'lm1'],
             'tue': ['lt0', 'lt1'],
             'wed': ['lw0', 'lw1']}}

out(oldSort)
out()

newSort = {}

for place in oldSort:
    for day in oldSort[place]:
        if not day in newSort:
            newSort[day] = dict()
        newSort[day][place] = list()
        for item in oldSort[place][day]:
            newSort[day][place].append(item)
        out(newSort)

out(newSort)
             
outfile.close()
