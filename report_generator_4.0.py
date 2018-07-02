#!/usr/bin/ env python3

# Imports
# -------

output = list()
errlog = list()

from argparse import ArgumentParser

# Parameters
# ----------

parser = ArgumentParser(fromfile_prefix_chars='@', 
                        description="read a timelog and generate a report")
parser.add_argument("-i", "--interactive", action="store_true", 
                    help="interactive mode")
parser.add_argument("-m", "--mail", action="store_true",
                    help="send report via email")
                    
args = parser.parse_args()




# Write output
# ------------

if errlog:
    outfile = open("errlog.txt", "w", encoding="utf-8")
    for entry in errlog:
        try:
            outfile.write(entry)
        except:
            outfile.write(format(entry))
        outfile.write("\n")
    outfile.close()
    
# The actual outfile will be formatted using the dates evaluated.
# All this later.

# Final readln
# ------------

readln = input("Press enter to exit program.")
