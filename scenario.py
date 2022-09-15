import websockets
import asyncio
 
async def listen(url: str):
    async with websockets.connect(url) as ws:
        while True:
            dist = await ws.recv()
            sign = await ws.recv()
            print(dist)
            if float(dist) <= 20 :
                await ws.send ("STOP")
            elif int(sign) < 500 and int(sign) > 300:
                await ws.send("TURN")
            else:
                await ws.send("ADVANCE")

asyncio.get_event_loop().run_until_complete(listen("ws://192.168.183.34:1234"))
