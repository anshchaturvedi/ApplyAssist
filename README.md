# ApplyAssist

An automated job application tracker which scans your emails!

Try it like so:

```
python3 quickstart.py
```

Currently my classifier is trained on my own emails and I don't want to share them, so it won't work for you. I am working on a way to train it on your own emails, but it's not ready yet.

## How it works
I use the Gmail API to get all my emails, then I use spaCy to classify them as one of "rejected", "acknowledged" or "neither". Currently the code will only output a dictionary of the email and what the model thinks it is, but I am working on a way to output it to a more usable format like JSON, so that I could turn it into an API and use it in a frontend.
