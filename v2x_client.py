import websockets
import asyncio
import socket



def v2x(host: str, port: int):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host,port))
        msg = "What Am i supposed to do ?"
        s.send(msg.encode())
        resp = s.recv(1024)
        s.close()
    return(resp)
 
async def listen(url: str):
    async with websockets.connect(url) as ws:
        i = 0
        while True:
            dist = await ws.recv()
            sign = await ws.recv()
            
            #print(dist)

            if float(dist) <= 20 :
                await ws.send ("STOP")

            elif int(sign) < 500 and int(sign) > 300 and i == 0:
                traject_instruction = v2x("127.0.0.1",2345).decode()
                i+=1
                print("you can only go: "+traject_instruction.upper())
                await ws.send("ADVANCE")

            elif int(sign) < 500 and int(sign) > 300 and i!=0:
                await ws.send("TURN")


            
            else:
                await ws.send("ADVANCE")

asyncio.get_event_loop().run_until_complete(listen("ws://140.93.8.250:1234"))