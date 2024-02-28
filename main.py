from werkzeug.datastructures import auth
from config import *
import flask
import dataclasses
import urllib.parse
import StateHandler
from typing import Callable
import asyncio

app = flask.Flask(
	__name__,
	static_url_path="",
	static_folder="web/static",
	template_folder="web/templates"
)

state = StateHandler.State()

@state.state_changed
def state_changed(state: StateHandler.State):
	track: (StateHandler.Track | None) = state.now_playing
	if track is None:
		# Clear RPC
		return

	# Set RPC

def generate_auth_url() -> str:
	event_endpoint = flask.url_for("event")
	webhook_url = f"http://{ADDRESS}:{PORT}{event_endpoint}"
	
	params = {
		"applicationName": APP_NAME,
		"userApiUrl": webhook_url
	}
	auth_url = "https://web-scrobbler.com/webhook?" + urllib.parse.urlencode(params)
	return auth_url

@app.route("/event", methods=[ "POST" ])
def event():
	if not flask.request.is_json:
		return flask.make_response("No JSON body", 400)

	state.handle_event(flask.request.json)
	return flask.make_response("OK")

@app.route("/", methods=[ "GET" ])
def index():
	return flask.render_template("index.j2")

@app.route("/now-playing", methods=[ "GET" ])
def now_playing_ui():
	return flask.render_template(
		"now-playing.j2",
		track=state.now_playing,
		auth_url=generate_auth_url()
	)

if __name__ == "__main__":
	app.run(
		debug=False,
		host=ADDRESS,
		port=PORT
	)