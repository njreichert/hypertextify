"""
parser.py
By Nikolaus J. Reichert - nikolaus@njreichert.ca

Detects, parses, and groups stringlist lines as different types
of Markdown format types.

"""

from enum import Enum, auto
from linegroup import BlockType, ElementContainer, LinkContainer
import re
from typing import Text # For Regexes.

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
    CODE = auto() # Codeblock.
    
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
        # and should be dealt with as a block. Otherwise, inline.
        LINK:"^\[.*\]\(.*\)$", # Matches any text enclosed by "[]()".
        IMG:"^!\[.*\]\(.*\)$", # Matches LINK, with a ! prepended.

        CODE:"^(\t| {4}).*", # Matches Tab/spaces, then anything.
        TEXT:"." # All characters. A last resort.
    }

    """
    Inline Element regexes.
    """
    inlineExprs = {
        LINK:"\[.*\]\(.*\)", # Matches any text enclosed by "[]()".
        IMG:"!\[.*\]\(.*\)" # Matches LINK, with a ! prepended.
    }

"""
Determines the LineDescriptor best associated with the given string.

Parameters: 
text: The string to evaluate.

Return Value:
classification: Of type LineDescriptor
"""
def classifyString(text):
    for descriptor, expr in LineDescriptor.matchExprs:
        if re.fullmatch(expr, text.strip()):
            return descriptor
    
    return None # If we get here, something has gone horribly wrong.

"""
Grabs the link and alt-text from an image or link string.

Parameters:
text: The string in question. 

Return values:
None if classifyString(text) != IMG or LINK

Otherwise...
link: The link found in the string.
altText: The alt-text in the string.
"""
def extractLink(text):

    # Check for a non-link type.
    if (classifyString(text) != LineDescriptor.LINK and \
        classifyString(text) != LineDescriptor.IMG):
            return None

    # Grab the text inside [these brackets].
    altText = re.search("?<=\[).*(?=\])", text)[0]

    # Grab the text inside (these parentheses).
    link = re.search("(?<=\().*(?=\))", text)[1]

    return link, altText

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

    # Gives the parser context as to what to do with the string. 
    previousLineType = LineDescriptor.BLANK 
    currentLineType = LineDescriptor.BLANK

    lineList = []
    parsedList = []

    linePointer = 0 # Zero-indexed line number.

    while(linePointer < len(inputBuffer)):
        previousLineType = currentLineType
        currentLineType = classifyString(inputBuffer[linePointer])

        # Figure out what to do with the current line.
        if (currentLineType == LineDescriptor.TEXT):
            # Add to used text, and look for
            # a "terminator" or more lines of text.
            lineList.append(inputBuffer[linePointer])
            linePointer += 1
            continue
    
        if (currentLineType == LineDescriptor.BLANK):
            if (previousLineType == LineDescriptor.TEXT):
                newElement = ElementContainer(lineList, BlockType.PARAGRAPH)
                parsedList.append(newElement)
                lineList.clear()
                linePointer += 1
                continue

            if (previousLineType == LineDescriptor.QUOTE):
                newElement = ElementContainer(lineList, BlockType.QUOTE)
                parsedList.append(newElement)
                lineList.clear()
                linePointer += 1
                continue

        if (currentLineType == LineDescriptor.QUOTE):
            lineList.append(inputBuffer[linePointer])
            linePointer += 1
            continue

        if (currentLineType == LineDescriptor.IMG or LineDescriptor.LINK):
            if (previousLineType == LineDescriptor.TEXT):
                # Deal with it when doing inline elements.
                lineList.append(inputBuffer[linePointer])
                linePointer += 1
                continue

            # Otherwise...
            link, altText = extractLink(inputBuffer[linePointer])
            parsedList.append(LinkContainer(altText, currentLineType, link))
            linePointer += 1
            continue

    return parsedList
    