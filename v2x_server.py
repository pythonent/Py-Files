from picarx import Picarx
import websockets
import time
import math
import asyncio

px = Picarx()

port  = 1234
print("Server currently listening on port: ",port)



async def echo(websocket, path):
    i = 0
    while True:
        line_percept = px.get_grayscale_data()
        val = line_percept[0]
        ultrasonic_percept = int(px.ultrasonic.read())
        
        await websocket.send(str(ultrasonic_percept))
        await websocket.send(str(val))
        
        resp = await websocket.recv()
        print(resp)
        if resp == "ADVANCE": #and resp == prec and old_prec == prec:
            px.forward(1)
        elif resp == "TURN" and i == 0:
            px.set_dir_servo_angle(-18)
            px.forward(1)
            time.sleep(1.25)
            px.set_dir_servo_angle(0)
            i+=1
        elif resp == "TURN" and i == 1:
            px.set_dir_servo_angle(20)
            px.forward(1)
            time.sleep(1)
            px.set_dir_servo_angle(0)
            i+=1
        elif resp == "TURN" and i == 2:
            px.set_dir_servo_angle(-20)
            px.forward(1)
            time.sleep(1.75)
            px.set_dir_servo_angle(0)   
            i+=1
        else:
            px.stop
            while resp != "ADVANCE":
                distance = int(px.ultrasonic.read())
                await websocket.send(str(distance))
                line_percept = px.get_grayscale_data()
                val = line_percept[0]
                await websocket.send(str(val))
                resp = await websocket.recv()
                px.stop() 
    px.stop()       

start_server = websockets.serve(echo,"140.93.8.250",port)

asyncio.get_event_loop().run_until_complete(start_server)

asyncio.get_event_loop().run_forever()
         
