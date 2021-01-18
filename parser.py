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
    TEXT = auto() # If the last read datatype is a paragraph or header.
    QUOTE = auto()
    HEADER = auto()
    LIST = auto()
    LINK = auto()
