from __future__ import print_function

import base64
import os.path
from pprint import pprint
import time
import subprocess
import extractor
import sys

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
USER_ID = "me"

def main():
    # get MAX_RESULTS from the command line
    MAX_RESULTS = int(sys.argv[1])
    
    # delete all the test files
    subprocess.call("rm test*.html", shell=True)

    creds = get_credentials()

    start_time = time.time()
    service = build("gmail", "v1", credentials=creds)

    # use the gmail API to get the latest 5 messages
    results = service.users().messages().list(userId=USER_ID, maxResults=MAX_RESULTS, q="category:primary").execute()
    
    # get the messages from the response
    messages = results.get("messages", [])

    parts_count = 0
    body_count = 0

    # for each message id, get the message
    for idx, message in enumerate(messages):
        mime_types = ["multipart/alternative", "multipart/mixed"]
        response_format = "full"

        response = service.users().messages().get(userId=USER_ID, id=message["id"], format=response_format).execute()
        mime_type = response["payload"]["mimeType"]

        if mime_type in mime_types:
            for p in response["payload"]["parts"]:
                if p["mimeType"] in ["text/plain", "text/html"]:
                    data = base64.urlsafe_b64decode(p["body"]["data"]).decode("utf-8")
                    f = open(f"test{idx}.html", "a")
                    f.write(data)
                    f.close()
                    parts_count += 1

        # this is when the message is not multipart
        else:
            a = response["payload"]["body"]["data"]
            data = base64.urlsafe_b64decode(a).decode("utf-8")
            f = open(f"test{idx}.html", "a")
            f.write(data)
            f.close()
            body_count += 1

    end_time = time.time()
    
    # print the time taken to extract the text formatted as ss:ms
    print(f"Time taken: {end_time - start_time:.2f}s")

    # extract text from the html files and rewrite the files with the extracted text
    for idx in range(MAX_RESULTS):
        with open(f"test{idx}.html", "r") as f:
            content = f.read()
            text = extractor.extract_text(content)
            f.close()
        with open(f"test{idx}.html", "w") as f:
            f.write(text)
            f.close()

def get_credentials():
    """Gets valid user credentials from storage. Pulled straight from Google API docs."""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds

if __name__ == "__main__":
    main()
