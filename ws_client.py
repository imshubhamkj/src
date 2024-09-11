import websocket
import json

file_metadata = None
file_data = b''

def on_message(ws, message):
    global file_metadata, file_data

    # Check if the message is a string (JSON data or file metadata)
    if isinstance(message, str):
        try:
            data = json.loads(message)  # Try to parse the message as JSON
            if "file_name" in data:
                # If it's file metadata, prepare to receive the file
                file_metadata = data
                print(f"Receiving file: {file_metadata['file_name']} ({file_metadata['file_size']} bytes)")
            else:
                # It's JSON file content
                print("Received JSON data:", data)
        except json.JSONDecodeError:
            print(f"Received unknown text message: {message}")

    # If the message is binary, it's part of the file (CSV or Excel)
    elif isinstance(message, bytes):
        file_data += message  # Append binary data

        # Check if the entire file is received
        if file_metadata and len(file_data) >= file_metadata['file_size']:
            save_file(file_metadata['file_name'], file_data)
            ws.close()

def save_file(file_name, file_data):
    with open(file_name, 'wb') as f:
        f.write(file_data)
    print(f"File saved as {file_name}")

def on_open(ws):
    print("Connection opened")
    # Send a message to request a specific file (either JSON, CSV, or Excel)
    ws.send("request_json")  # Request a JSON file
    # ws.send("request_csv")  # Uncomment to request a CSV file
    # ws.send("request_excel")  # Uncomment to request an Excel file

def on_error(ws, error):
    print(f"Error: {error}")

def on_close(ws, close_status_code, close_msg):
    print("Connection closed")

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://localhost:8888/websocket",
                                on_open=on_open,
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    
    ws.run_forever()
