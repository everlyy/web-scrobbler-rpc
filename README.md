# Web Scrobbler Discord RPC

This is a small program to show your currently playing song as your Discord status.

# Quick Start

First you need to add a Webhook to your Web Scrobbler accounts,
you can do that by allowing access [over here](https://web-scrobbler.com/webhook?applicationName=Everly's%20Discord%20RPC&userApiUrl=http://localhost:8080) or with these steps:
 1. Go to Web Scrobbler's settings
 2. Go to the 'Accounts' tab
 3. Scroll down to where it says 'Webhook'
 4. Add a new webhook, 'Application name' doesn't matter, this can be anything
 6. API URL should be what you set up in `config.py`, if you didn't change this it's `http://localhost:8080`

Then you need to start the webhook server. Make sure you have python3 and pip installed.
Then you can install the required packages like this:
```console
$ pip install flask
```

Then you can run `main.py` with python
```console
$ python3 main.py
```
