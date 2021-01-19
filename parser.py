"""
parser.py
By Nikolaus J. Reichert - nikolaus@njreichert.ca

Detects, parses, and groups stringlist lines as different types
of Markdown format types.

"""

from enum import Enum, auto
import re # For Regexes.

"""
Denotes the most recent datatype evaluated. Allows it to keep track
of what it is searching for.
"""
class LineDescriptor(Enum):
    BLANK = auto() # If there is nothing parsed yet.
    TEXT = auto() # Paragraph or header. A last resort
    QUOTE = auto()
    HEADER = auto() # Match 
    H1LINE = auto() # The underline for a header.
    H2LINE = auto()
    LIST = auto()
    LINK = auto() # some form of link.
    IMG = auto() # link, but with a '!' prepended.
    
    """
    Regexes denoting Block-level elements.
    """
    matchExprs = {
        # Blank Regex attrib: https://stackoverflow.com/a/52267453
        BLANK:"^$", # Match nothing. Unused.
        QUOTE:"> .+", # Match a quote, space, then 1 or more chars.
        HEADER:"^#{1,6} .+", # 1-6 hash signs, space, and 1+ chars.
        H1LINE:"^=+$", # ONLY 1 or more '='
        H2LINE:"^-+$", # 1 or more -'s
        LIST:"^[-\+\*] .+", # Match any line starting with "-+* "
        # Either of these can occur as the only text on the line, 
        # and should be dealt with accordingly.
        LINK:"^\[.*\]\(.*\)$", # Matches any text enclosed by "[]()".
        IMG:"^!\[.*\]\(.*\)$", # Matches LINK, with a ! prepended.
        TEXT:"." # All characters. Probably unused?
    }

    """
    Inline Element regexes.
    """
    inlineExprs = {
        LINK:"\[.*\]\(.*\)", # Matches any text enclosed by "[]()".
        IMG:"!\[.*\]\(.*\)" # Matches LINK, with a ! prepended.
    }



"""
Creates a list of partly-parsed ElementContainers that can be
parsed for inline elements.

Parameters:
inputBuffer: The text to be parsed. Expects a list of strings
    representing each line.

Return Value:
parsedList: The list of ElementContainers.
"""
def createContainerList(inputBuffer):
    mode = ParserMode.BLANK # Tells the parser what to do next.
    parsedList = []
    linePointer = 0 # Zero-indexed line number.

    while(linePointer < len(inputBuffer)):
        # Figure out what to do with the current line.
        mode = classifyString(inputBuffer[linePointer])

        if (mode == ParserMode.BLANK):
            linePointer += 1
            continue

    return parsedList
    