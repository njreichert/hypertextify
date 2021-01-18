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
class ElementContainer:
    """
    Constructor.

    Parameters: 
    contents: A list of any type.
    containerType: expects FormatType
    """
    def __init__(self, contents, containerType):
        self.contents = contents
        self.containerType = containerType

    """
    Appends an element to contents.

    Parameters:
    item: the item to append to contents.
    """
    def append(self, item):
        self.contents.append(item)

    """
    Formats container into the relevant HTML tags.

    Return value: The HTML tags, as a string.
    """
    def __str__(self):
        formattedText = "" # Container for format.
        for item in self.contents:
            formattedText += item # TODO: Does this format as expected?
        
        # containerType is a format string.
        return self.containerType.format(text=formattedText)

"""
Special type of ElementContainer that also holds linking information.

Extends: ElementContainer.
"""
class LinkContainer(ElementContainer):
    """
    Constructor.

    Parameters:
    contents: Usually linktext or alt-text.  # TODO: Redefine into list.
    containerType: Expects LinkType.
    link: The link in question.
    """
    def __init__(self, contents, containerType, link):
        super().__init__(contents, containerType)
        self.link = link

    """
    Formats as string.

    Return value: The string in question.
    """
    def __str__(self):
        return str.format


"""
Represents different types of "container tags" to be implemented.
"""
class BlockType(Enum):
    PARAGRAPH = "<p>\n{text}\n</p>"
    CODEBLOCK = "<pre><code>\n{text}\n</code></pre>"
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
    
    INLINECODE = "<code>{text}</code>"
    BOLD = "<strong>{text}</strong>"
    ITALICS = "<em>{text}</em>"
    
"""
Represents special inline types that have more information
associated with them.
"""
class LinkType(Enum):
    LINK = "<a href=\"{link}\">{text}</a>"
    IMAGE = "<img src=\"{link}\" alt=\"{text}\">"
