from __future__ import print_function

import base64
import os.path
from pprint import pprint
import requests
import time
import subprocess

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def main():
    # delete all the test files
    subprocess.call("rm test*.html", shell=True)

    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
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

    try:
        # Call the Gmail API
        service = build("gmail", "v1", credentials=creds)
        user_id = "anshchaturvedi23@gmail.com"

        results = service.users().labels().list(userId=user_id).execute()
        labels = results.get("labels", [])

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"An error occurred: {error}")

    start_time = time.time()

    user_id = "anshchaturvedi23@gmail.com"
    headers = {
        "Authorization": f"Bearer {creds.token}",
        "Accept": "application/json",
    }
    max_results = 5
    query = "q=%5B%20in%3Ainbox%20-category%3A%7Bsocial%20promotions%20forums%7D%20%5D"

    response = requests.get(
        f"https://gmail.googleapis.com/gmail/v1/users/{user_id}/messages?maxResults={max_results}&q=category:primary",

        headers=headers,
    ).json()["messages"]

    parts_count = 0
    body_count = 0

    for idx, message in enumerate(response):
        message_id = message["id"]
        print(f"message_id: {message_id}")
        response_format = "full"
        response = requests.get(
            f"https://gmail.googleapis.com/gmail/v1/users/{user_id}/messages/{message_id}?format={response_format}",
            headers=headers,
        ).json()
        mime_type = response["payload"]["mimeType"]
        print(f"mimeType: {mime_type}")
        print(f"labelIds: {response['labelIds']}")
        print("-------------------")
        mime_types = ["multipart/alternative", "multipart/mixed"]


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
    print(f"parts_count: {parts_count}, body_count: {body_count}")
    print(f"Time taken: {end_time - start_time}")

if __name__ == "__main__":
    main()
