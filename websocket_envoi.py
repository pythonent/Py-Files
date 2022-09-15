import pickle
from sqlite3 import connect
import websockets
import asyncio
import cv2
import numpy as np
import imutils, struct
import os




port = 1235


print("Server listening on port: "+str(port))

connected = set()


async def echo(websocket, path):
    print("A client just connected")
    cap = cv2.VideoCapture(0)
    try:
        while(cap.isOpened()):
            ret,frame = cap.read()
            frame = imutils.resize(frame,width=320)
            a = pickle.dumps(frame)
            message = struct.pack("Q",len(a))+a
            await websocket.send(message)
            resp = await websocket.recv()
            print(resp)
    except websocket.exception.ConnectionClosed as e:
        print("Client disconnected !")
    finally:
        websocket.close()
            

start_server = websockets.serve(echo,"localhost",port)

asyncio.get_event_loop().run_until_complete(start_server)

asyncio.get_event_loop().run_forever()