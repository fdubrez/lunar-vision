from typing import Callable, List
from urllib.parse import urlencode

import socketio
from pydantic import BaseModel

from models import LanderAction, LanderData


class Query(BaseModel):
    clientName: str 
    clientUuid: str
    clientEmoji: str
    clientColor: str
    
    def __str__(self):
        return urlencode(dict(self))
 
class Client(BaseModel):
    """ client lunar-lander """
    server: str
    query: Query
    handleLander : Callable[[List[LanderData]], LanderAction]

    def start(self) -> None:
        sio = socketio.Client()

        @sio.event
        def connect() -> None:
            print('connection established')

        @sio.event
        def disconnect() -> None:
            print('disconnected from server')

        @sio.event
        def landersData(payload) -> None:
            action = self.handleLander(
                [LanderData.parse_obj(data) for data in payload]
            )
            sio.emit('playerActions', action.export())

        print(f"{self.server}?{self.query}")
        sio.connect(f"{self.server}?{self.query}")
        sio.wait()
