"""
linegroup.py
By Nikolaus J. Reichert - nikolaus@njreichert.ca

Implements an enum for format types and a class for
groups of lines that will be within the same HTML tag.
"""

from enum import Enum, auto

"""
A container of strings or inline elements that will be rendered as a part.
"""
# TODO

"""
Contains an inline-formatted string.
"""
# TODO

"""
Represents different types of text to be implemented.

"""
class FormatType(Enum):
    PARAGRAPH = "<p>\n{text}\n</p>"
    CODEBLOCK = "<pre>\n{text}\n<code>"
    QUOTE = "<blockquote>\n{text}\n</blockquote>"
    ORDEREDLIST = "<ol>\n{text}\n</ol>"
    UNORDEREDLIST = "<ul>\n{text}\n</ul>"
    LISTITEM = "<li>\n{text}\n</li>"
    TEXT = "{text}" # For pasting pure HTML.
    H1 = "<h1>\n{text}\n</h1>"
    H2 = "<h2>\n{text}\n</h2>"
    H3 = "<h3>\n{text}\n</h3>"
    H4 = "<h4>\n{text}\n</h4>"
    H5 = "<h5>\n{text}\n</h5>"
    H6 = "<h6>\n{text}\n</h6>"

"""
Represents different types of inline elements that can be
added into the file.
"""
class InlineType(Enum):
    LINK = "<a>{text}</a>"
    INLINECODE = "<code>{text}</code>"
    BOLD = "<strong>{text}</strong>"
    ITALICS = "<em>{text}</em>"


