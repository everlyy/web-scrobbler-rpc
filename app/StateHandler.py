import dataclasses
from typing import Callable

@dataclasses.dataclass
class Track:
	title: str
	artist: str
	album: (str | None)
	cover: (str | None)
	start_time: int
	connector: str

class State:
	def __init__(self):
		self.now_playing: (Track | None) = None
		self._state_changed_handlers: list[Callable] = []

	def _parse_track_from_event(self, event: dict):
		song = event["data"]["song"]
		info = song["processed"]
		metadata = song["metadata"]

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

		return Track(
			title=info["track"],
			artist=info["artist"],
			album=info.get("album"),
			start_time=int(metadata["startTimestamp"]),
			connector=connector,
			cover=cover
		)

	def handle_event(self, event):
		event_name = event["eventName"]
		is_something_playing = event_name in ("nowplaying", "resumedplaying", "scrobble")

		self.now_playing = (
			None
			if not is_something_playing else
			self._parse_track_from_event(event)
		)

		for handler in self._state_changed_handlers:
			handler(self)

	def state_changed(self, func):
		self._state_changed_handlers.append(func)