#!/usr/bin/env python3

# This will retrieve summary reports from the toggl API for consecutive weeks
# and store the logged times by project for further comparisons.

# Imports
# -------

from pprint import pprint
from datetime import date,datetime,timedelta
from TogglPy import Toggl # https://github.com/matthewdowney/TogglPy
toggl = Toggl()
from time import sleep



# Variables
# ---------

firstMonday = date(2017,8,28)
firstSunday = date(2017,9,3)
# dates for API tests
firstMonday = date(2018,11,5)
firstSunday = date(2018,11,11)


dayDelta = timedelta(1,0,0)

curMonday = firstMonday
curSunday = firstSunday

testOutput = []
#testOutput = [{'mon': '12766-03-1', 'sun': '12766-03-7', 'times': {'coding': '15:00:00', 'writing': '15:00:00', 'reading': '15:00:00', 'gaming': '15:00:00'}}, {'mon': '12766-03-8', 'sun': '12766-03-14', 'times': {'coding': '15:00:00', 'writing': '15:00:00', 'reading': '15:00:00', 'gaming': '15:00:00'}}, {'mon': '12766-03-15', 'sun': '12766-03-21', 'times': {'coding': '15:00:00', 'writing': '15:00:00', 'reading': '15:00:00', 'gaming': '15:00:00'}}, {'mon': '12766-03-22', 'sun': '12766-03-28', 'times': {'coding': '15:00:00', 'writing': '15:00:00', 'reading': '15:00:00', 'gaming': '15:00:00'}}]

datalog = []
projectList = []

idPath = "data/id.txt"
idVals = {}
idFile = open(idPath, "r", encoding="utf-8")
idPath = idFile.readline().strip()
idFile.close()
idFile = open(idPath, "r", encoding="utf-8")
for line in idFile:
    line = line.strip().split("::")
    idKey = line[0]
    idVal = line[1]
    idVals[idKey] = idVal
#testOutput.append(idVals)
toggl.setAPIKey(idVals["token"])


# loop through consecutive weeks
# ------------------------------

while curSunday <= date.today():

    # create dict entry
    # -----------------
    curWeek = {}
    curWeek["Mon"] = curMonday
    curWeek["Sun"] = curSunday
    curWeek["times"] = {}

    requestParams = {
        "workspace_id": idVals["id"],
        "user_agent": idVals["uagent"],
        "grouping": "projects",
        "since": curMonday,
        "until": curSunday,
    }

    response = toggl.request("https://toggl.com/reports/api/v2/summary",
                parameters=requestParams)
    print("retrieved {} - {}. Sleeping...".format(curMonday,curSunday))
    #testOutput.append(response["data"])
    #testOutput.append("="*50)
    sleep(2)
    testOutput.append(curMonday)

    responseData = response["data"]
    for item in responseData:
        curProject = item["title"]["project"]
        curTime = item["time"]
        #testOutput.append(item["time"])
        #testOutput.append(item["title"]["project"])
        testOutput.append(curProject)
        testOutput.append(curTime)
        if not curProject in projectList:
            projectList.append(curProject)



    datalog.append(curWeek)

    # move to next week
    # -----------------
    curMonday += dayDelta * 7
    curSunday += dayDelta * 7

    

datalog.append(projectList)






# write to output file

with open("./data/compareWeeksJson.txt","w",encoding="utf-8") as outfile:
    pprint(testOutput,outfile)
    outfile.write("\n{}\n".format("="*60))
    pprint(datalog,outfile)

