from __future__ import print_function

import base64
import os.path
from pprint import pprint
import time
import subprocess
import extractor
import credentials
import sys

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def main():
    # get MAX_RESULTS from the command line
    MAX_RESULTS = int(sys.argv[1])

    USER_ID = "me"
    test_directory = "test_files"

    # delete all the test files
    subprocess.call(f"rm -rf {test_directory}", shell=True)

    os.makedirs(test_directory, exist_ok=True)

    creds = credentials.get_credentials()

    start_time = time.time()
    service = build("gmail", "v1", credentials=creds)

    results = (
        service.users()
        .messages()
        .list(userId=USER_ID, maxResults=MAX_RESULTS, q="category:primary")
        .execute()
    )
    messages = results.get("messages", [])

    parts_count = 0
    body_count = 0

    # for each message id, get the message
    for idx, message in enumerate(messages):
        mime_types = ["multipart/alternative", "multipart/mixed"]
        response_format = "full"

        response = (
            service.users()
            .messages()
            .get(userId=USER_ID, id=message["id"], format=response_format)
            .execute()
        )
        mime_type = response["payload"]["mimeType"]
        file_path = os.path.join("test_files", f"test{idx}.html")

        if mime_type in mime_types:
            for p in response["payload"]["parts"]:
                if p["mimeType"] in ["text/plain", "text/html"]:
                    data = base64.urlsafe_b64decode(p["body"]["data"]).decode("utf-8")
                    f = open(file_path, "a")
                    f.write(data)
                    f.close()
                    parts_count += 1

        # this is when the message is not multipart
        else:
            a = response["payload"]["body"]["data"]
            data = base64.urlsafe_b64decode(a).decode("utf-8")
            f = open(file_path, "a")
            f.write(data)
            f.close()
            body_count += 1

    end_time = time.time()

    # print the time taken to extract the text formatted as ss:ms
    print(f"Time taken: {end_time - start_time:.2f}s")

    # extract text from the html files and rewrite the files with the extracted text
    for idx in range(MAX_RESULTS):
        file_path = os.path.join(test_directory, f"test{idx}.html")
        with open(file_path, "r") as f:
            content = f.read()
            text = extractor.extract_text(content)
            f.close()
        with open(file_path, "w") as f:
            f.write(text)
            f.close()


if __name__ == "__main__":
    main()
