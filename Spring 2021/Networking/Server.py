import asyncio
import socket
import threading
import time

SERVER_LOGGING = True


class TestServer():
    def __init__(self, host, port, timeout=3):
        self.listen_thread = threading.Thread(target=self.__listen)
        self.isListening = threading.Event()
        self.host = host
        self.port = port
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.settimeout(timeout)
        self.client_timeout = 1
        self.server.bind((host, port))
        self.connections = []

    def start_listening(self):
        if not self.isListening.is_set():
            self.isListening.set()
            self.listen_thread.start()
            print(f"Server started listening on: '{self.host}'::{self.port}")

    def stop_listening(self):
        self.isListening.clear()

    def __listen(self):
        self.server.listen()
        while self.isListening.is_set():
            try:
                conn = self.server.accept()
                conn[0].settimeout(self.client_timeout)
                self.connections.append(conn)
                if SERVER_LOGGING:
                    print(f"New connection {conn[1][0]}")
            except socket.timeout:
                pass

    def respond_echo(self):
        client_socket: socket.socket
        for connection_data in self.connections:
            client_socket = connection_data[0]
            try:
                msg = client_socket.recv(255).decode('utf8')
                client_socket.send(f"I got {msg}".encode('utf8'))
                # yield msg
            except socket.timeout:
                pass


    # pass in a function whose argument is a string.
    # return value of function will be a response to whatever input was recieved
    def callback_respond(self, callback):
        client_socket: socket.socket
        for connection_data in self.connections:
            client_socket = connection_data[0]
            try:
                msg = client_socket.recv(255).decode('utf8')
                response = callback(msg) # we expect the response to be encoded
                client_socket.send(response)
            except socket.timeout:
                pass
    def send_data(self, connection, msg):
        client_socket: socket.socket
        client_socket = self.connections[connection]
        try:
            client_socket.send(msg)
        except socket.timeout:
            if SERVER_LOGGING:
                print("Socket Timeout in send_data")

# sample, used as an example for callback_respond
def echo_callback(msg):
    return f"Echo'd {msg}".encode('utf8')



if __name__ == '__main__':
    server = TestServer('localhost', 33933)
    server.start_listening()
    time.sleep(5)
    server.stop_listening()
    print("Stopped listening")
    while True:
        server.callback_respond(echo_callback)
