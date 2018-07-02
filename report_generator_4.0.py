#!/usr/bin/ env python3

# Imports
# -------

from argparse import ArgumentParser

# Parameters
# ----------

parser = ArgumentParser(fromfile_prefix_chars='@', 
                        description="read a timelog and generate a report")
parser.add_argument("-i", "--interactive", action="store_true", 
                    help="interactive mode")
                    
args = parser.parse_args()





# Final readln
# ------------

readln = input("Press enter to exit program.")