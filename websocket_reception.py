from asyncio.windows_events import NULL
import pickle
import websockets
import asyncio
import cv2
import numpy as np
import imutils, struct
import time

async def listen():
    url = "ws://140.93.11.190:1235"

    async with websockets.connect(url) as ws:
        try:
            data = b""
            #f_start = 0
            #f = 0
            payload_size = struct.calcsize("Q")
            classNames = []
            classFile = 'coco.names'

            with open(classFile,'rt') as f:
                classNames = f.read().rstrip('\n').split('\n')
            #print(classNames)
            configPath = "ssd_mobilenet_v3_large_coco_2020_01_14.pbtxt"
            weightsPath = "frozen_inference_graph.pb"
            net = cv2.dnn_DetectionModel(weightsPath, configPath)
            net.setInputSize(320,320)
            net.setInputScale(1.0/127.5)
            net.setInputMean((127.5, 127.5, 127.5))
            net.setInputSwapRB(True)

            while True:
                while len(data) < payload_size:
                    packet = await ws.recv()
                    if not packet: break
                    data += packet
                packed_msg_size = data[:payload_size]
                data = data[payload_size:]
                msg_size = struct.unpack("Q",packed_msg_size)[0]

                while len(data) < msg_size:
                    data += await ws.recv()
                frame_data = data[:msg_size]
                data = data[msg_size:]
                img = pickle.loads(frame_data)
                classIds, confs, bbox = net.detect(img, confThreshold=0.6
                )
                print(classIds,bbox)
                if len(classIds) == 0:
                    await ws.send('ADVANCE')
                else:
                    for a in classIds:
                        if a == 13:
                            await ws.send('STOP')
                """f_end = time.time()
                t_diff = f_end - f_start
                f = 1/(t_diff)
                f_start = f_end
                f_text = "FPS: {:.1f}".format(f)
                cv2.putText(img,f_text,(5,30),cv2.FONT_HERSHEY_COMPLEX, 1,(0,255,255),1)"""
                cv2.imshow('output',img)
                cv2.waitKey(1)
        except websockets.exceptions.ConnectionClosed as e:
            print("No data received")
            


asyncio.get_event_loop().run_until_complete(listen())
