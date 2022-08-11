import difflib
from difflib import HtmlDiff

debugLogFailure = open("/home/smoothex/Desktop/test_python_failure/debug.log").readlines()
debugLogNormal = open("/home/smoothex/Desktop/test_python_normal/debug.log").readlines()

delta = difflib.Differ().compare(debugLogNormal, debugLogFailure)

# Create an HTML file showing the differences between the 2 files
delta_html = HtmlDiff(wrapcolumn=270).make_file(debugLogNormal, debugLogFailure)
with open("diff.html", "w") as f:
    f.write(delta_html)
    # File is now located in the same directory as this python file
