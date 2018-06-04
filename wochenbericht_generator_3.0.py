#!/usr/bin/env python3

import re
from datetime import date, time, timedelta, datetime
#from collections import OrderedDict

datum_format = "%y-%m-%d"
uhrzeit_format = "%H:%M:%S"

errlog = []

# Select evaluated projects
# -------------------------

# projects = ["Programmieren", "Lernen", "Uni", "Papa", "Organisation", "Schlafen"]
projects = ["Organisation", "Programmieren", "Organisation - geteilt", "Organisation - privat", "Programmieren - privat" ]

def optionSelection(optionList):
    returnString = ""
    for item in optionList:
        returnString += "{} {}\n".format(optionList.index(item), item)
    return returnString

promptDefault = "0,1"     # replace with a list or tuple at some point?
promptForProjects = input("Select projects by typing the respective numbers:\n(default: {})\n{}".format(promptDefault, optionSelection(projects)))
if promptForProjects == "": promptForProjects = promptDefault

selectedProjects = list()

for i in range(len(projects)):
    if str(i) in promptForProjects:
        selectedProjects.append(projects[i])
        
print("Diese Projekte werden evaluiert:")
print(selectedProjects)
#print("") # blank line

# find correct dates; set up intermediate storage
# -----------------------------------------------

wochenliste = list()
tag = timedelta(1,0,0)
datum = date.today() - ( date.weekday(date.today()) * tag )
datum = datum - ( tag * 7 )  # change week for test purposes

for i in range(7):
    tageintrag = dict()
    tageintrag["Datum"] = datum
    tageintrag["Bericht"] = dict()
    tageintrag["Aufgaben"] = list()
    tageintrag["Gesamtdauer"] = timedelta(0,0,0)
    wochenliste.append(tageintrag)
    datum += tag
    
#print(wochenliste)

# read the report log
# -------------------

bericht = open("C:/Users/HAL/Dropbox/org-161014/fortschrittsbericht.txt", "r", encoding="utf-8")

befind_regexp = r""" 
        \s* bbb \s* 
        (\d{2}-\d{2}-\d{2}) # Datum
        \s+ (?: - \s+ )?
        (:-[)/(])               # Befindlichkeit
        \s+ (?: - \s+ )?
        ( .+? )                 # Kommentar
        (?: \s* ccc )?
        \s*$
        """

for line in bericht:
    if "bbb" in line:
        #print(line.rstrip())
        eval = re.match(befind_regexp, line, re.X)
        if not eval:
            # print("{}\n error: malformed line".format(line.rstrip()))
            errlog.append("error: malformed line\n")
            errlog.append(line)
            continue
        #print(eval.groups())
        #for i in range(len(eval.groups())):
            #print(i+1, eval.group(i+1))
        datum = datetime.strptime(eval.group(1), datum_format).date()
        #print(datum)
        
        tageintrag = False
        for entry in wochenliste:
            if entry["Datum"] == datum:
                tageintrag = entry
        if not tageintrag:
            continue
        
        #print(tageintrag)
        tageintrag["Bericht"]["smiley"] = eval.group(2)
        #tageintrag["Bericht"]["kommentar"] = eval.group(3)
        kommentar = eval.group(3)
        # if "ccc" in kommentar:    # workaround for my regex difficulties
            # komeval = re.match(r"(.+)\s*ccc\.*", kommentar)
            # kommentar = komeval.group(1)
        tageintrag["Bericht"]["kommentar"] = kommentar
        
        #print(tageintrag)
        
bericht.close()

#print("test dictionary after reading report log")
#for item in logdict:
    #print(item,logdict[item])

# Read task log
# -------------
    
import csv

montag = wochenliste[0]["Datum"]
sonntag = wochenliste[6]["Datum"]
tasklog = "C:/Users/HAL/Downloads/Toggl_time_entries_{}_to_{}.csv".format(montag, sonntag)
reader = csv.DictReader(open(tasklog, "r", encoding="utf-8"))

for row in reader:
    # print(row)

    #print(row["Project"])
    if not row["Project"] in selectedProjects:
        #print("not in selected projects")
        continue
    #else:
        #print("is a selected project")

    #for item in row:
    #print(item, row[item])

    taskentry = dict()
    taskentry["Projekt"] = row["Project"]
    taskentry["Beschreibung"] = row["Description"]
    
    datum = datetime.strptime(row["Start date"], "%Y-%m-%d").date()
    start_time = datetime.strptime(row["Start time"], uhrzeit_format).time()
    end_time = datetime.strptime(row["End time"], uhrzeit_format).time()
    duration = datetime.strptime(row["Duration"], uhrzeit_format)
    duration = timedelta(hours=duration.hour, minutes=duration.minute, seconds = duration.second)
    
    #taskentry["Datum"] = datum
    taskentry["Startzeit"] = start_time
    taskentry["Endzeit"] = end_time
    taskentry["Dauer"] = duration

    for entry in wochenliste:
        if entry["Datum"] == datum:
            #print(entry)
            entry["Aufgaben"].append(taskentry)
            entry["Gesamtdauer"] += duration
    
    # Todo: Verifizieren, dass die Taskliste in der richtigen Reihenfolge ausgegeben wird


#print("Check dictionary after adding tasks:")
# ---------------------------------------------
# import pprint
# pp = pprint.PrettyPrinter()
# pp.pprint(wochenliste)
#import json
#printWochenliste = wochenliste
#print(json.dumps(printWochenliste, indent=4))

# Write Output
# ------------

output = open("C:/Users/HAL/Downloads/wochenbericht_{}_to_{}.txt".format(montag, sonntag), "w", encoding="utf-8")

for line in errlog:
    output.write(line)

separator = "\n{}\n\n".format("=" * 60)

output.write(separator)

gesamtdauer = timedelta()

for entry in wochenliste:
    gesamtdauer += entry["Gesamtdauer"]
#print(gesamtdauer)

output.write("Gesamtzeit diese Woche: {}\n".format(gesamtdauer))

for entry in wochenliste:
    
    output.write(separator)
    output.write("{}\n".format(entry["Datum"].strftime("%a %d. %m. %y")))   # someday: Wochentage auf deutsch ausgeben

    # Wenn Aufgabenliste, dann nach Bericht suchen, Ausgabe etc.
    if entry["Bericht"]:
        output.write("\n")
        if entry["Gesamtdauer"]:
            output.write("Gesamtzeit: {}\n".format(entry["Gesamtdauer"]))
        for item in entry["Bericht"]:
            output.write("{}: {}\n".format(item, entry["Bericht"][item]))
        if not entry["Aufgaben"]:
            output.write("*** Achtung: Bericht gefunden, aber keine Aufgabenliste. ***\n")
            continue
    else:
        if entry["Aufgaben"]:
            output.write("*** Achtung: Aufgabenliste gefunden, aber kein Bericht. ***\n")
        else:
            output.write("Keine Aufzeichnungen\n")
            continue
    
    output.write("\nAufgaben:\n")
    for task in entry["Aufgaben"]:
        output.write("----\n")
        for field in task:
            output.write("{}: {}\n".format(field, task[field]))

    
    
output.close()
