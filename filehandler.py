"""
Filehandler.py
By Nikolaus J. Reichert - nikolaus@njreichert.ca

Handles file I/O.

"""

"""
Opens the file, intreprets it as a string list,
and closes it, returning the string list.

Parameters: fileName (Name of file).

Return value: fileText.
"""
def openFile(fileName):
    fileText = [] # The read lines of the file.
    inputFile = open(fileName, "rt")
    
    for line in inputFile:
        fileText.append(line)
    
    inputFile.close()

    return fileText


f = openFile("test.md")

for line in f:
    print("{", line, "}")
