import asyncio
import os
import uuid

from brain import Brain
from client import Client, Query

PLAYER_NAME = os.getenv('PLAYER_NAME', 'intrepyx')

def start():
    brain = Brain(player_name=PLAYER_NAME)

    client = Client(
        server = os.getenv('SERVER_URL', 'http://127.0.0.1:4000/'),
        query = Query(
            clientName =  PLAYER_NAME,
            clientUuid = str(uuid.uuid1()), 
            clientEmoji = os.getenv('PLAYER_EMOJI', "🚀" ),
            clientColor = os.getenv('PLAYER_COLOR', '00FF00')
        ),
        handleLander = brain.handleLander
    )

    asyncio.run(client.start())

if __name__ == "__main__":
    start()