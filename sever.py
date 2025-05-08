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