# websocket_server1.py
import tornado.ioloop
import tornado.web
import tornado.websocket
import json

class WebSocketHandler(tornado.websocket.WebSocketHandler):
    def open(self):
        print("WebSocket connection opened")

    def on_message(self, message):
        print(f"Received message from client: {message}")
        # When a message is received, send the JSON file
        if message == "send_json":
            self.send_json_file()

    def send_json_file(self):
        try:
            # Load the JSON file
            with open('data.json', 'r') as f:
                json_data = json.load(f)
            
            # Send JSON data to the client
            self.write_message(json.dumps(json_data))
        except FileNotFoundError:
            self.write_message("Error: JSON file not found.")
        except Exception as e:
            self.write_message(f"Error: {str(e)}")

    def on_close(self):
        print("WebSocket connection closed")

    def check_origin(self, origin):
        # Allow connections from any origin
        return True

def make_app():
    return tornado.web.Application([
        (r"/websocket", WebSocketHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("Tornado WebSocket server started on ws://localhost:8888/websocket")
    tornado.ioloop.IOLoop.current().start()
