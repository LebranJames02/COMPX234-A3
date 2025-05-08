# 服务器代码 server.py
import socket
import threading
import time


class TupleSpace:
    def __init__(self):
        self.tuples = {}
        self.lock = threading.Lock()
        self.client_count = 0
        self.operation_count = 0
        self.read_count = 0
        self.get_count = 0
        self.put_count = 0
        self.error_count = 0

    def put(self, key, value):
        with self.lock:
            if key in self.tuples:
                self.error_count += 1
                return 1
            self.tuples[key] = value
            self.put_count += 1
            return 0

    def read(self, key):
        with self.lock:
            if key not in self.tuples:
                self.error_count += 1
                return ""
            self.read_count += 1
            return self.tuples[key]

    def get(self, key):
        with self.lock:
            if key not in self.tuples:
                self.error_count += 1
                return ""
            value = self.tuples.pop(key)
            self.get_count += 1
            return value

    def get_summary(self):
        with self.lock:
            tuple_count = len(self.tuples)
            total_tuple_size = sum(len(key) + len(value) for key, value in self.tuples.items())
            total_key_size = sum(len(key) for key in self.tuples.keys())
            total_value_size = sum(len(value) for value in self.tuples.values())
            avg_tuple_size = total_tuple_size / tuple_count if tuple_count > 0 else 0
            avg_key_size = total_key_size / tuple_count if tuple_count > 0 else 0
            avg_value_size = total_value_size / tuple_count if tuple_count > 0 else 0
            summary = (
                f"Tuple count: {tuple_count}, "
                f"Avg tuple size: {avg_tuple_size}, "
                f"Avg key size: {avg_key_size}, "
                f"Avg value size: {avg_value_size}, "
                f"Client count: {self.client_count}, "
                f"Operation count: {self.operation_count}, "
                f"READs: {self.read_count}, "
                f"GETs: {self.get_count}, "
                f"PUTs: {self.put_count}, "
                f"Errors: {self.error_count}"
            )
            return summary

    def handle_client(client_socket, tuple_space):
        tuple_space.client_count += 1
        while True:
            try:
                request = client_socket.recv(1024).decode()
                if not request:
                    break
                size = int(request[:3])
                operation = request[4]
                key = request[6:size - 1] if operation != 'P' else request[6:size - len(request.split()[-1]) - 2]
                value = request[size - len(request.split()[-1]) - 1:] if operation == 'P' else ""

                tuple_space.operation_count += 1
                if operation == 'P':
                    result = tuple_space.put(key, value)
                    if result == 0:
                        response = f"{str(len(f'OK ({key}, {value}) added') + 3).zfill(3)} OK ({key}, {value}) added"
                    else:
                        response = f"{str(len(f'ERR {key} already exists') + 3).zfill(3)} ERR {key} already exists"
                elif operation == 'R':
                    result = tuple_space.read(key)
                    if result:
                        response = f"{str(len(f'OK ({key}, {result}) read') + 3).zfill(3)} OK ({key}, {result}) read"
                    else:
                        response = f"{str(len(f'ERR {key} does not exist') + 3).zfill(3)} ERR {key} does not exist"
                elif operation == 'G':
                    result = tuple_space.get(key)
                    if result:
                        response = f"{str(len(f'OK ({key}, {result}) removed') + 3).zfill(3)} OK ({key}, {result}) removed"
                    else:
                        response = f"{str(len(f'ERR {key} does not exist') + 3).zfill(3)} ERR {key} does not exist"
                else:
                    response = f"{str(len('ERR invalid operation') + 3).zfill(3)} ERR invalid operation"
                    tuple_space.error_count += 1

                client_socket.send(response.encode())
            except Exception as e:
                print(f"Error handling client: {e}")
                break
        client_socket.close()

    def main():
        if len(sys.argv) != 2:
            print("Usage: python server.py <port>")
            sys.exit(1)

        port = int(sys.argv[1])
        tuple_space = TupleSpace()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            # 设置端口复用，避免程序重启时端口占用问题
            server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server_socket.bind(('0.0.0.0', port))
            server_socket.listen(10)
            print(f"Server listening on port {port}")

