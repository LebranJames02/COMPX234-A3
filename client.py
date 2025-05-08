# 客户端代码 client.py
import socket
import sys
def send_request(client_socket, request):
    # 发送请求消息
    client_socket.send(request.encode())
    # 接收响应消息
    response = client_socket.recv(1024).decode()
    return response
def main():
    if len(sys.argv) != 4:
        print("Usage: python client.py <hostname> <port> <request_file>")
        sys.exit(1)

    hostname = sys.argv[1]
    port = int(sys.argv[2])
    request_file = sys.argv[3]