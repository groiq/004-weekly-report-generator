Weekly Report Generator - v4
============================

primäres Ziel: Die Einträge über das API holen.

es gibt einen "stillen" und einen interaktiven Modus. Der stille Modus benutzt Default-Einstellungen: vergangene Woche; evaluiert werden alle "Arbeit"-Einträge.

Hat toggl eine Keyword-Funktion?

files to check:
004-weekly-report-generator\wochenbericht_generator_3.0.py
var_kandidaten\arbeitszeitVergleich.py
002-process-duration-calculator for setup of interactive mode

various goals:

create project list dynamically

more flexible project list

a script to delete breaks

Auxiliary programs:

An auxiliary will be a seperate .py script that implements a part of the functionality, so I won't have to navigate through the entire file at once.


Temporarily read the data from a local file, instead of fetching from toggl every time.

Write a daily resumee. I have a file of running notes. 

When I first start the computer on a new day, insert a datestamp into the notes. (Automate later.)

One resumee per day and project. (Maybe override later?)

If no resumee is found, prompt.

Why id and pid in data?

