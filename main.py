from __future__ import print_function

import base64
import credentials
import extractor
import os.path
import subprocess
import sys
import time

from googleapiclient.discovery import build


def main():
    rejections = "(thank you AND regret) OR (thank you AND unfortunately) -{resident services, ppl, support, richa, change.org, energy, pr, michelle, rent, tldr, network, quora, cnet, medium, aliexpress, liz, parkrun, sheridan}) "
    acknowledgements = "received your application -{nathan, monster, shein, romwe, linkedin, uber, tim hortons, oil, skillshare, network, quora, cnet, medium, aliexpress, liz, parkrun, sheridan}"
    neither = "category:primary"
    user_id = "me"

    creds = credentials.get_credentials()

    service = build("gmail", "v1", credentials=creds)

    # get_and_save_messages(
    #     service, user_id, 32, rejections, "full", "rejections"
    # )
    # get_and_save_messages(
    #     service, user_id, 32, acknowledgements, "full", "acknowledgements"
    # )

    # get_and_save_messages(service, user_id, 32, neither, "full", "neither")


def get_and_save_messages(
    service, user_id, max_results, query, response_format, directory
) -> None:
    """
    Gets the messages from the Gmail API and saves them to the test_files directory.
    """
    start_time = time.time()

    subprocess.call(f"rm -rf {directory}", shell=True)
    os.makedirs(directory, exist_ok=True)

    results = (
        service.users()
        .messages()
        .list(userId=user_id, maxResults=max_results, q=query)
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
            .get(userId=user_id, id=message["id"], format=response_format)
            .execute()
        )
        mime_type = response["payload"]["mimeType"]
        file_path = os.path.join(directory, f"test{idx}.txt")
        # print snippets of the message
        print(f"{response['snippet']}\n")

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
            if "data" not in response["payload"]["body"]:
                continue
            a = response["payload"]["body"]["data"]
            data = base64.urlsafe_b64decode(a).decode("utf-8")
            f = open(file_path, "a")
            f.write(data)
            f.close()
            body_count += 1

    # extract text from the html files and rewrite the files with the extracted text
    for the_file in os.listdir(directory):
        file_path = os.path.join(directory, the_file)
        with open(file_path, "r") as f:
            content = f.read()
            text = extractor.extract_text(content)
            f.close()
        with open(file_path, "w") as f:
            f.write(text)
            f.close()

    end_time = time.time()

    # print the time taken to extract the text formatted as ss:ms
    print(f"Time taken: {end_time - start_time:.2f}s")


if __name__ == "__main__":
    main()
