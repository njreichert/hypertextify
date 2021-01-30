"""
parser.py
By Nikolaus J. Reichert - nikolaus@njreichert.ca

Detects, parses, and groups stringlist lines as different types
of Markdown format types.

"""

from enum import Enum, auto
from linegroup import *
import re
from typing import Text # For Regexes.

"""
Regexes denoting Block-level elements.
"""
matchExprs = {
    # Blank Regex attrib: https://stackoverflow.com/a/52267453
    ElementType.ANY:".",
    ElementType.NONE:"^$", # Match nothing. Unused.
    ElementType.QUOTE:"> .+", # Match a quote, space, then 1 or more chars.
    ElementType.H1:"^# .+", # 1-4 hash signs, space, and 1+ chars.
    ElementType.H2:"^## .+", # 1-4 hash signs, space, and 1+ chars.
    ElementType.H3:"^### .+", # 1-4 hash signs, space, and 1+ chars.
    ElementType.H4:"^#### .+", # 1-4 hash signs, space, and 1+ chars.
    ElementType.UNORDEREDLIST:"^- .+", # Match any line starting with "- "
    
    # Either of these can occur as the only text on the line, 
    # and should be dealt with as a block. Otherwise, inline.
    LinkType.LINK:"^\[.*\]\(.*\)$", # Matches any text enclosed by "[]()".
    LinkType.IMAGE:"^!\[.*\]\(.*\)$", # Matches LINK, with a ! prepended.
    
    ElementType.CODEBLOCK:"^(\t| {4}).*", # Matches Tab/spaces, then anything.
    ElementType.TEXT:".+" # All characters. A last resort.
}

"""
Inline Element regexes.
"""
inlineExprs = {
    LinkType.LINK:"\[.*\]\(.*\)", # Matches any text enclosed by "[]()".
    LinkType.IMAGE:"!\[.*\]\(.*\)" # Matches LINK, with a ! prepended.
}


"""
Elements that should be interpreted immediately
as an element.
"""
oneLiners = [
    LinkType.LINK,
    LinkType.IMAGE,
    ElementType.H1,
    ElementType.H2,
    ElementType.H3,
    ElementType.H4,
]


"""
Determines the ElementType best associated with the given string.

Parameters: 
text: The string to evaluate.

Return Value:
classification: Of type ElementType
"""
def classifyString(text):
    for descriptor, expr in matchExprs.items():
        print(descriptor, expr)
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
    if (classifyString(text) != LinkType.LINK and \
        classifyString(text) != LinkType.IMAGE):
            return None

    # Grab the text inside [these brackets].
    altText = re.search("(?<=\[).*(?=\])", text).group()

    # Grab the text inside (these parentheses).
    link = re.search("(?<=\().*(?=\))", text).group()

    return link, altText


"""
Removes all markdown from the given list of lines..

Parameters:
lineList: The string list in question.

Return Value:
lineList: TODO
"""
def extractText(lineList):
    return lineList # TODO


"""
Creates an element from a given string list and
appends it to the given list.

Parameters:
elementList: The list of elements to append to.
lineList: The string list in question.
elementType: Expects ElementType or LinkType.
"""
def addElement(elementList, lineList, elementType):
    if (elementType.__class__ == LinkType):
        # extractLink expects a line, rather than a list of lines.
        linkInfo = extractLink(lineList[0]) 
        newElement = LinkContainer(linkInfo[1], elementType, linkInfo[0])
        elementList.append(newElement)
    elif (elementType.__class__ == ElementType):
        newElement = ElementContainer(extractText(lineList), elementType)
        elementList.append(newElement)


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
    previousLineType = ElementType.NONE
    currentLineType = ElementType.NONE

    lineList = []
    parsedList = []

    for line in inputBuffer:
        previousLineType = currentLineType
        currentLineType = classifyString(line)

        if (currentLineType != previousLineType or currentLineType in oneLiners):
            # Only add previous lines to a new element
            # if they have text to add.
            if (previousLineType != ElementType.NONE):
                addElement(parsedList, extractText(lineList).copy(), previousLineType)
                lineList.clear()

        # Skip all blank lines.
        if (currentLineType == ElementType.NONE):
            continue
        else:
            lineList.append(line)

    # Process last element if there is any lines not terminated properly.
    # Files should end with a newline in proper formatting.
    if (len(lineList) > 0):
        addElement(parsedList, extractText(lineList), previousLineType)
        lineList.clear()


    return parsedList
