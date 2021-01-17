"""
Filehandler.py
By Nikolaus J. Reichert - nikolaus@njreichert.ca

Handles file I/O.

"""

"""
Opens a file, intreprets it as a string list,
and closes it, returning the string list.

Parameters: fileName (Name of file).

Return value: fileText.
"""
def interpretFile(fileName):
    fileText = [] # The read lines of the file.
    inputFile = open(fileName, "rt")
    
    for line in inputFile:
        strippedLine = line.rstrip('\n') # Remove all newlines.
        fileText.append(strippedLine)
    
    inputFile.close()
    return fileText



# Test area.
f = interpretFile("test.md")

for line in f:
    print("{", line, "}", sep="")
