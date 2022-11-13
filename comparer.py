import difflib
from difflib import HtmlDiff
import os

user = os.getenv("USER", default=None)
bug_number = '13346'  # or one of the other tickets

debugLogFailure = open("/home/"+user+"/Desktop/"+bug_number+"_failure/debug.log").readlines()
debugLogNormal = open("/home/"+user+"/Desktop/"+bug_number+"_normal/debug.log").readlines()

delta = difflib.Differ().compare(debugLogNormal, debugLogFailure)

# Create an HTML file showing the differences between the 2 files
delta_html = HtmlDiff(wrapcolumn=270).make_file(debugLogNormal, debugLogFailure)
with open("diff.html", "w") as f:
    f.write(delta_html)
    # File is now located in the same directory as this python file
