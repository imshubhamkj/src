import tornado.ioloop
import tornado.web
import tornado.websocket
import os

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("WebSocket connection opened")

    def on_message(self, message):
        print(f"Received message from client: {message}")
        
        # Handle the message, if it's a request for a file download
        if message == "download_file":
            self.send_file()

    def send_file(self):
        try:
            # Specify the file path to send
            file_path = 'sample_file.xlsx'  # Example file path (can be any file)
            file_size = os.path.getsize(file_path)
            file_name = os.path.basename(file_path)
            file_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"  # MIME type for an Excel file
            
            # Send metadata first
            metadata = {
                "file_name": file_name,
                "file_size": file_size,
                "file_type": file_type
            }
            self.write_message(metadata)

            # Send file in chunks if necessary, otherwise as a single binary message
            with open(file_path, 'rb') as f:
                while True:
                    chunk = f.read(4096)  # Read the file in 4KB chunks
                    if not chunk:
                        break
                    self.write_message(chunk, binary=True)

        except FileNotFoundError:
            self.write_message({"error": "File not found"})
        except Exception as e:
            self.write_message({"error": str(e)})

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
