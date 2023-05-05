from __future__ import print_function

import os.path
import pprint
import requests

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


def main():
    """Shows basic usage of the Gmail API.
    Lists the user's Gmail labels.
    """
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

        if not labels:
            print("No labels found.")
            return
        print("Labels:")
        for label in labels:
            print(label["name"])

    except HttpError as error:
        # TODO(developer) - Handle errors from gmail API.
        print(f"An error occurred: {error}")

    user_id = "anshchaturvedi23@gmail.com"
    headers = {
        "Authorization": "Bearer ya29.a0AWY7CkmaK2Cgp2PtdL0jxG7Eih_G4WhQoZGPAAbf7dwkhXomtIQ9AsxYPf_wI3HfsCJRgR81Elr_vuWcl_L_5kKF2V9BZeLhwdblKequkgpFAEHMalTuwj2m8vF0v3ghXBJ2D7Hw-_oTD_sGvjTv05fYEKq-aCgYKAV4SARASFQG1tDrpZO23bSpVPCW9xoZOVIbpGA0163",
        "Accept": "application/json",
    }

    response = requests.get(
        f"https://gmail.googleapis.com/gmail/v1/users/{user_id}/messages", headers=headers
    )
    pprint.pprint(response.json())


if __name__ == "__main__":
    main()
