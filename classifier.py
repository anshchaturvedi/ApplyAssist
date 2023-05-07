"""
This module contains the functions that are used to classify the text that is
extracted from the html files.

It is a tri-class classifier that classifies the text into one of the following
categories:
    1. Acknowledgement of a job/internship application
    2. Rejection of a job/internship application
    3. None of the above
"""

import os


# first we need to convert each text file into a single string
def get_text(file_path: str) -> str:
    """
    Returns the text from the file as a string.
    """
    f = open(file_path, "r")
    lines = f.readlines()
    return multiline_to_single_line(lines)


def multiline_to_single_line(lines: list[str]) -> str:
    """
    Returns a single line string from the list of lines.
    """
    lines = [line.strip() for line in lines]
    single_line = " ".join(lines)
    return single_line


acknowledgements, rejections, neither = [], [], []
# for all files in the acknowledgement folder, get the text and add it to the
# list of texts
for the_file in os.listdir("acknowledgements"):
    file_path = os.path.join("acknowledgements", the_file)
    acknowledgements.append(get_text(file_path))

for the_file in os.listdir("rejections"):
    file_path = os.path.join("rejections", the_file)
    rejections.append(get_text(file_path))

for the_file in os.listdir("neither"):
    file_path = os.path.join("neither", the_file)
    neither.append(get_text(file_path))

# print(f"Number of acknowledgement emails: {len(acknowledgements)}")
# print(f"Number of rejection emails:       {len(rejections)}")
# print(f"Number of other emails:           {len(neither)}")

import spacy
import classy_classification

data = {
    "acknowledgements": acknowledgements,
    "rejections": rejections,
    "neither": neither,
}

nlp = spacy.blank("en")
nlp.add_pipe(
    "text_categorizer",
    config={
        "data": data,
        "model": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2",
        "device": "gpu",
    },
)

print(nlp("we've received your application! Wait for a response from us!")._.cats)
