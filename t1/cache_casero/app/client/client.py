import grpc
import cache_service_pb2
import cache_service_pb2_grpc

class CacheClient:
    def __init__(self, host="master", port=50051):
        self.channel = grpc.insecure_channel(f"{host}:{port}")
        self.stub = cache_service_pb2_grpc.CacheServiceStub(self.channel)

    def put(self, key, value):
        response = self.stub.Put(cache_service_pb2.CacheItem(key=key, value=value))
        print(response.message)

    def get(self, key):
        response = self.stub.Get(cache_service_pb2.Key(key=key))
        if response.value:  # Comprobar si hay un valor, en lugar de 'exists'
            return response.value
        else:
            print("Key not found.")
            return None

    def remove(self, key):
        response = self.stub.Remove(cache_service_pb2.Key(key=key))
        print(response.message)

if __name__ == "__main__":
    client = CacheClient()

    