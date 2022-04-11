import json
import os
import select
import traceback
import websocket

websocket._logging._logger.level = -99
from ipc.ipc_message_handler import IPCMessageHandler

from ipc.ipc_message import IPCMessage

POLL_DELAY_MS = 10


class IPCPipe:
    def __init__(self, address, message_handler: IPCMessageHandler):
        self.message_handler = message_handler
        self.ws = websocket.WebSocketApp(
            address,
            on_message=(lambda ws, message: self.on_message(ws, message)),
            on_error=(lambda ws, error: self.on_error(ws, error)),
            on_open=(lambda ws: self.on_open(ws)),
            on_close=(
                lambda ws, close_status_code, close_msg: self.on_close(
                    ws, close_status_code, close_msg
                )
            ),
        )

        self.ws.run_forever()

    def send_message(self, type: int, body: str = None, id: str = None):
        self.ws.send(IPCMessage(type, body, id).toJSON())

    def on_message(self, ws: websocket.WebSocket, message):
        msg = json.loads(message, object_hook=lambda d: IPCMessage(**d))
        self.message_handler.handle_message(self, msg)

    def on_error(self, ws: websocket.WebSocket, error):
        print("Websocket error: ", error)
        print("".join(traceback.format_stack()))

    def on_close(self, ws: websocket.WebSocket, close_status_code, close_msg):
        print("Websocket Closed")

    def on_open(self, ws: websocket.WebSocket):
        print("Websocket Opened")
