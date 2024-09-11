import tornado.ioloop
import tornado.web
import tornado.websocket
import json
import os

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("WebSocket connection opened")

    def on_message(self, message):
        print(f"Message received from client: {message}")

        # Parse the client message to determine which file type to send
        if message == "request_json":
            self.send_json_file()
        elif message == "request_csv":
            self.send_csv_file()
        elif message == "request_excel":
            self.send_excel_file()
        else:
            self.write_message("Invalid request")

    def send_json_file(self):
        # Sample JSON data to send
        json_data = {
            "name": "Example",
            "data": [1, 2, 3, 4, 5]
        }
        # Convert the dictionary to a JSON string and send it
        json_message = json.dumps(json_data)
        self.write_message(json_message)
        print("Sent JSON file to client")

    def send_csv_file(self):
        try:
            # Path to the CSV file
            file_path = 'sample_file.csv'
            file_size = os.path.getsize(file_path)
            file_name = os.path.basename(file_path)
            file_type = "text/csv"

            # Send file metadata as JSON
            metadata = {
                "file_name": file_name,
                "file_size": file_size,
                "file_type": file_type
            }
            self.write_message(json.dumps(metadata))

            # Send CSV file in chunks (binary mode)
            with open(file_path, 'rb') as f:
                while True:
                    chunk = f.read(4096)
                    if not chunk:
                        break
                    self.write_message(chunk, binary=True)
            print("Sent CSV file to client")

        except FileNotFoundError:
            self.write_message(json.dumps({"error": "CSV file not found"}))
        except Exception as e:
            self.write_message(json.dumps({"error": str(e)}))

    def send_excel_file(self):
        try:
            # Path to the Excel file
            file_path = 'sample_file.xlsx'
            file_size = os.path.getsize(file_path)
            file_name = os.path.basename(file_path)
            file_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            
            # Send file metadata as JSON
            metadata = {
                "file_name": file_name,
                "file_size": file_size,
                "file_type": file_type
            }
            self.write_message(json.dumps(metadata))

            # Send Excel file in chunks (binary mode)
            with open(file_path, 'rb') as f:
                while True:
                    chunk = f.read(4096)
                    if not chunk:
                        break
                    self.write_message(chunk, binary=True)
            print("Sent Excel file to client")

        except FileNotFoundError:
            self.write_message(json.dumps({"error": "Excel file not found"}))
        except Exception as e:
            self.write_message(json.dumps({"error": str(e)}))

    def on_close(self):
        print("WebSocket connection closed")

    def check_origin(self, origin):
        return True  # Allow connections from any origin

def make_app():
    return tornado.web.Application([
        (r"/websocket", WebSocketHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Tornado WebSocket server started on ws://localhost:8888/websocket")
    tornado.ioloop.IOLoop.current().start()
