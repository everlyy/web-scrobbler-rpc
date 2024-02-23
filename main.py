import pypresence
import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from config import *

rpc = pypresence.Presence(
	client_id=DISCORD_CLIENT_ID
)

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
			small_text=connector,
			start=start_time
		)
	except Exception as e:
		print(f"Couldn't update RPC: {e}")
		rpc_try_connect()

class WebScrobblerWebhookServer(BaseHTTPRequestHandler):
	def do_POST(self):
		r = json.loads(
			self.rfile.read(
				int(self.headers["Content-Length"])
			)
		)
		self.send_response(200)

		update_rpc(r)

if __name__ == "__main__":
	rpc_try_connect()
	server = HTTPServer((ADDRESS, PORT), WebScrobblerWebhookServer)
	print(f"HTTP server started on {ADDRESS}:{PORT}")

	try:
		server.serve_forever()
	except KeyboardInterrupt:
		pass

	rpc.close()
	server.server_close()