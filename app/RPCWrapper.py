import discordrp

class RPCWrapper:
    def __init__(self, client_id):
        self.client_id = client_id
        self._rpc: (discordrp.Presence | None) = None

    def _connect(self):
        if self._rpc is None:
            try:
                self._rpc = discordrp.Presence(self.client_id)
            except Exception as e:
                print(f"Couldn't connect to Discord RPC: {e}")
                self._rpc = None

    def _is_connected(self):
        if self._rpc is None:
            self._connect()

        return self._rpc is not None

    def clear(self, *args, **kwargs):
        if self._is_connected():
            try:
                return self._rpc.clear(*args, **kwargs)
            except Exception as e:
                print(f"Couldn't clear Discord RPC: {e}")
                self._rpc = None

    def set(self, *args, **kwargs):
        if self._is_connected():
            try:
                return self._rpc.set(*args, **kwargs)
            except Exception as e:
                print(f"Couldn't clear Discord RPC: {e}")
                self._rpc = None