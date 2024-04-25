import json
from websocket import WebSocketApp

assets = 'btcusdt@kline_1m'

def on_message(ws,message):
    message = json.loads(message)
    manipulation(message)

# socket = "wss://stream.binance.com:9443/stream?streams="+assets
socket = "wss://fstream.binance.com/stream?streams="+assets

prevData = 0
writeFileCount = 0


def writeData(rel_data):
    with open("btc.txt", "w") as f:
        f.write(str(rel_data))

def manipulation(source):
    global prevData
    global writeFileCount
    rel_data = source["data"]['k']['c']
    # once started save data
    if writeFileCount == 0:
        writeData(rel_data)
    writeFileCount += 1
    print(rel_data)
    if writeFileCount == 3:
        writeData(rel_data)
        writeFileCount = 1
    
ws = WebSocketApp(socket, on_message=on_message)
ws.run_forever()
