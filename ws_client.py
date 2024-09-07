import websocket
import json

file_metadata = None
file_data = b''

def on_message(ws, message):
    global file_metadata, file_data

    # If the message is a string, it might be metadata
    if isinstance(message, str):
        try:
            metadata = json.loads(message)  # Try parsing JSON metadata
            if "file_name" in metadata:
                file_metadata = metadata
                print(f"Receiving file: {file_metadata['file_name']} ({file_metadata['file_size']} bytes)")
            elif "error" in metadata:
                print(f"Error: {metadata['error']}")
        except json.JSONDecodeError:
            print(f"Received unknown message: {message}")

    # If the message is binary, it's part of the file data
    elif isinstance(message, bytes):
        file_data += message  # Append binary data to the file_data

        # If we have received the entire file, save it
        if len(file_data) >= file_metadata['file_size']:
            save_file(file_metadata['file_name'], file_data)
            ws.close()

def save_file(file_name, file_data):
    with open('file_name.xlsx', 'wb') as f:
        f.write(file_data)
    print(f"File saved as {file_name}")

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("Connection closed")

def on_open(ws):
    print("Connection opened")
    # Request the file download
    ws.send("download_file")

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:8888/websocket",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    
    ws.run_forever()
