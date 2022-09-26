import difflib

debugLogFailure = open("/home/smoothex/Desktop/13337_failure/debug.log").readlines()
debugLogNormal = open("/home/smoothex/Desktop/13337_normal/debug.log").readlines()

diff = []

# all ERROR lines that don't appear in the CORRECT execution
for errorLine in debugLogFailure:
    if errorLine not in debugLogNormal:
        # print(errorLine)
        diff.append(errorLine)

"""
# all NORMAL lines that don't appear in the WRONG execution
for normalLine in debugLogNormal:
    if normalLine not in debugLogFailure:
        # print(errorLine)
        diff.append(normalLine)
"""
print("\n".join(diff))

# save the differences to a file
with open('difference-13337.txt', 'w') as file_out:
    for line in diff:
        file_out.write(line)
