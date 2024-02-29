from config import *
import flask
import RPCWrapper
import StateHandler
import urllib.parse

app = flask.Flask(
	__name__,
	static_url_path="",
	static_folder="web/static",
	template_folder="web/templates"
)

rpc = RPCWrapper.RPCWrapper(DISCORD_CLIENT_ID)
state = StateHandler.State()

@state.state_changed
def state_changed(state: StateHandler.State):
	track: (StateHandler.Track | None) = state.now_playing
	if track is None:
		rpc.clear()
		return

	rpc_state = {
		"details": track.title,
		"state": f"by {track.artist}",
		"assets": {
			"small_image": "ws",
			"small_text": f"{track.connector} connector"
		},
		"timestamps": {
			"start": track.start_time
		}
	}

	if track.cover is not None:
		rpc_state["assets"]["large_image"] = track.cover
	
	if track.album is not None:
		rpc_state["assets"]["large_text"] = track.album

	rpc.set(rpc_state)

def generate_auth_url() -> str:
	event_endpoint = flask.url_for("event")
	webhook_url = f"http://{flask.request.host}{event_endpoint}"
	
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