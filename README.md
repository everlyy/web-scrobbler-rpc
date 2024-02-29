# Web Scrobbler Discord RPC

This is a small program to show your currently playing song as your Discord status.

# Quick Start

Make sure you have python3 and pip installed.

Then you can install the required packages like this:
```console
$ pip install discord-rich-presence flask
```

Then you can run the app with python. This will start a web server which by default you can access at http://localhost:8080/
```console
$ python3 app/main.py
```

If you open the site in your browser you'll be prompted to authenticate the Webhook URL, do this and you should be good to go.

# Thanks

Big thanks to [Web Scrobbler](https://web-scrobbler.com/) for making such an awesome extension!
They also have a upcoming official RPC, I will link this here whenever it's public.
