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