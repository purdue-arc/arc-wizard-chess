import socket

if __name__ == '__main__':
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('localhost', 33933))
    client.setblocking(True)
    request = None
    while True:
        request = input('Send: ')
        client.send(request.encode('utf-8'))
        print("Waiting for response")
        response = client.recv(255).decode('utf-8')
        print(response)
