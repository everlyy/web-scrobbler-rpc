import pypresence
from config import *
import flask

rpc = pypresence.Presence(
	client_id=DISCORD_CLIENT_ID
)

app = flask.Flask(__name__)

def rpc_try_connect():
	try:
		rpc.connect()
		print(f"Connected to Discord RPC")
	except Exception as e:
		print(f"Couldn't connect to Discord RPC: {e}")

def update_rpc(r):
	evt = r["eventName"]
	playing = evt in ("nowplaying", "resumedplaying", "scrobble")

	print(f"Received event: {repr(evt)} {playing=}")

	if not playing:
		print(f"Nothing seems to be playing, clearing RPC")
		rpc.clear()
		return

	song = r["data"]["song"]
	info = song["processed"]
	metadata = song["metadata"]

	title = info["track"]
	artist = info["artist"]
	album = info.get("album")
	start_time = int(metadata["startTimestamp"])
	connector = (
		song["connectorLabel"]
		if "connectorLabel" in song else
		song["connector"]["label"]
	)
	cover = (
		metadata["trackArtUrl"]
		if "trackArtUrl" in metadata else
		song["parsed"]["trackArt"]
	)

	print(f"Currently playing: {artist} - {title}")

	try:
		rpc.update(
			details=title,
			state=f"by {artist}",
			large_image=cover,
			large_text=album,
			small_image="ws",
			small_text=f"Web Scrobbler - {connector}",
			start=start_time
		)
	except Exception as e:
		print(f"Couldn't update RPC: {e}")
		rpc_try_connect()

@app.route("/", methods=[ "POST" ])
def index():
	if flask.request.method == "POST" and not flask.request.is_json:
		return flask.make_response("method POST requires JSON body", 400)

	update_rpc(flask.request.json)
	return flask.make_response("OK")

if __name__ == "__main__":
	app.run(
		debug=False,
		host=ADDRESS,
		port=PORT
	)