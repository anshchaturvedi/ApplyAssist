"""
This module contains the functions that are used to extract the text from the
html files that are downloaded from the Gmail API.
"""

import imaplib
from bs4 import BeautifulSoup


def extract_text(content) -> str:
    """
    Extracts the text from the html file and returns it as a string.
    """
    soup = BeautifulSoup(content, "html.parser")

    # this should remove all the script and style tags
    for script in soup(["script", "style"]):
        script.extract()

    # format the html to a more readable format
    text = soup.get_text()

    # make sure there are no extra newlines and spaces
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = "\n".join(chunk for chunk in chunks if chunk)

    return text
