import os
import sys
sys.path.append("C:/Users/paulv/AppData/Roaming/Python/Python311/site-packages")



import bpy
import threading
import asyncio
import queue
import uuid
import json
import websockets

from pathlib import Path

modules_path = Path(bpy.data.filepath).parent 

if str(modules_path) not in sys.path:
    sys.path.insert(0, str(modules_path))
        
import SyncModulesPython as SyncModules
from SyncModulesPython.Core.ModulesRegistry import ModulesRegistry
import SyncModulesPython
v3 = SyncModules.Vector3Module.Vector3Module(0)
print(v3)
print(SyncModulesPython)

print(ModulesRegistry)


def stop():
    print("stopping")

WS_URI = "ws://130.79.90.188:3000"

WS_QUEUE = queue.Queue()
UUID = uuid.uuid4()

def outputFn( data ):
    print(data)


registry = ModulesRegistry(outputFn)


class ClientNetwork:
    def __init__(self):
        self.websocket = None
        self.onMessageCallback = None
        
    async def connect(self, uri):
        self.websocket = await websockets.connect(uri)
        
    async def send(self, message):
        await self.websocket.send(message)
        
    def sendFn(self, message):
        asyncio.create_task(self.send(message))
        
    async def listen(self):
        try:
            async for message in self.websocket:
                print(f"thread: {message}")
                WS_QUEUE.put(message)
        except Exception as e:
            print(e)
            
client = ClientNetwork()


stop_event = threading.Event()

async def main_async():
    await client.connect(WS_URI)
    
    listen_task = asyncio.create_task(client.listen())
    
    ### server expects first message to provide UUID of client
    message = {
        "UUID": str( UUID )
    }
    await client.send(json.dumps(message))
    
    ### hardcoded for now
    ### server expects users to join an instance, only Instance UUID(0) exists
    message = {
        "scope": "SYSTEM",
        "senderUUID": str( UUID ),
        "payload": {
            "command": "INSTANCE_JOIN",
            "data": {
                "instanceUUID": str( uuid.UUID(int=0)),
                "userUUID": str( UUID )
            }
        }
    }
    
    await client.send(json.dumps(message))
    await asyncio.sleep(0.5)
    
    #while True:
        #await asyncio.sleep(1)
    
    try:
        while not stop_event.is_set():
            await asyncio.sleep(0.1)
    finally:
        print("main_async - killing loop")
        listen_task.cancel()
        if client.websocket is not None:
            await client.websocket.close()
        
        
def start_async_loop():
    print("start_async_loop")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main_async())
    finally:
        loop.close()
        
def start_thread():
    print("start_thread")
    t = threading.Thread(target=start_async_loop, daemon=True)
    t.start()
    return t
    
def process_queue():
    while not WS_QUEUE.empty():
        message = WS_QUEUE.get()
        
        print(f"main {message}")
        
        try:
            messageData = json.loads(message)
        except:
            continue
        
        scope = messageData.get("scope")
        print(f"main: {scope}")
        
        if scope == "MODULE":
            payload = messageData.get("payload")
            command = payload.get("command")
            if command == "UPDATE_TRANSFORM":
                print(command)
                transform = payload.get("data").get("transform")
                print(transform)
                translation = transform.get("translation")
                rotation = transform.get("rotation")
                camera = bpy.data.objects.get("Camera")
                print(camera)
                camera.location = ( translation[0], translation[1], translation[2])
                camera.rotation_mode = "QUATERNION"
                camera.rotation_quaternion = (rotation[3],rotation[0],rotation[1],rotation[2]) 
                print(rotation)
    return (1.0 / 120.0)

thread_ref = { "thread": None }
def start():
    print("start")
    thread_ref["thread"] = start_thread()
    print(thread_ref["thread"])
    bpy.app.timers.register(process_queue)

bpy.app.driver_namespace["start"] = start

def stop():
    print("stop")
    stop_event.set()
    bpy.app.timers.unregister(process_queue)
    #thread_ref["thread"].join()
    #if thread_ref["thread"].is_alive():
        #print("failed to kill thread")

bpy.app.driver_namespace["stop"] = stop

start()

#stop()