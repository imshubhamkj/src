# websocket_client1.py
import websocket
import json

def on_message(ws, message):
    # Handle message from server (JSON data or error)
    try:
        json_data = json.loads(message)
        print("Received JSON data from server:")
        print(json.dumps(json_data, indent=4))
    except json.JSONDecodeError:
        print(f"Received non-JSON message: {message}")

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("Connection closed")

def on_open(ws):
    print("Connection opened")
    # Send a message requesting the JSON file
    ws.send("send_json")

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:8888/websocket",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    
    ws.run_forever()
