"""
parser.py
By Nikolaus J. Reichert - nikolaus@njreichert.ca

Detects, parses, and groups stringlist lines as different types
of Markdown format types.

"""

from enum import Enum, auto

"""
Denotes the most recent datatype evaluated. Allows it to keep track
of what it is searching for.
"""
class ParserMode(Enum):
    BLANK = auto() # If there is nothing parsed yet.
    TEXT = auto() # Paragraph or header.
    QUOTE = auto()
    HEADER = auto()
    LIST = auto()
    LINK = auto()



"""
Creates a list of partly-parsed ElementContainers that can be
parsed for inline elements.

Parameters:
inputText: The text to be parsed. Expects a list of strings
    representing each line.

Return Value:
parsedList: The list of ElementContainers.
"""
def createContainerList(inputText):
    mode = ParserMode.BLANK # Tells the parser what to do next.

    for line in range(len(inputText)):
        mode = classifyString(line)
