import grpc
import socket
from concurrent import futures
from collections import OrderedDict
import uhashring
import cache_service_pb2_grpc
from cache_service_pb2 import Key, CacheItem, NodeInfo, Response
import argparse

class CacheServiceServicer(cache_service_pb2_grpc.CacheServiceServicer):
    def __init__(self, is_master=True, max_items=100):
        self.is_master = is_master
        self.nodes = []
        self.ring = uhashring.HashRing()
        self.cache = OrderedDict()
        self.max_items = max_items

    def RegisterNode(self, request, context):
        if not self.is_master:
            return Response(success=False, message="Not a master node")
        
        node = f"{request.ip}:{request.port}"
        self.nodes.append(node)
        self.ring.add_node(node)
        
        return Response(success=True, message=f"Node registered successfully")

    def DeregisterNode(self, request, context):
        if not self.is_master:
            return Response(success=False, message="Not a master node")

        node = f"{request.ip}:{request.port}"
        if node in self.nodes:
            self.nodes.remove(node)
            self.ring.remove_node(node)
            return Response(success=True, message="Node deregistered successfully")
        return Response(success=False, message="Node not found")


    def Get(self, request, context):
        if self.is_master:
            node = self.ring.get_node(request.key)
            print(f"Forwarding retrieval of key '{request.key}' to node: {node}")
            response = forward_request_to_slave(self, node, "Get", request)
            return response
        else:
            value = self.cache.get(request.key, None)
            print(f"Retrieving key '{request.key}:{value}' from local cache")
            if value:

                self.cache.move_to_end(request.key)
                return CacheItem(key=request.key, value=value)
            else:
                return CacheItem(key=request.key, value="")

    def Put(self, request, context):
        if self.is_master:
            all_nodes = self.ring.get_nodes()
            node = self.ring.get_node(request.key)
            print(f"Forwarding insertion of key '{request.key}' to node: {node}")
            print(f"All possible nodes: {all_nodes}")
            response = forward_request_to_slave(self, node, "Put", request)
            return response
        else:
            print(f"Inserting key '{request.key}' in local cache")
            if len(self.cache) >= self.max_items:
                self.cache.popitem(last=False)
            self.cache[request.key] = request.value
            return Response(success=True, message="Inserted successfully")


    def Remove(self, request, context):
        if self.is_master:
            node = self.ring.get_node(request.key)
            print(f"Forwarding retrieval of key '{request.key}' to node: {node}")
            response = forward_request_to_slave(self, node, "Remove", request)
            return response
        else:
            if request.key in self.cache:
                del self.cache[request.key]
                return Response(success=True, message="Removed successfully")
            return Response(success=False, message="Key not found")


def serve(is_master=True, port=50051):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    cache_service_pb2_grpc.add_CacheServiceServicer_to_server(CacheServiceServicer(is_master=is_master), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    if is_master:
        print (f"Master server started on port {port}")
    else:
        print (f"Slave server started on port {port}")
    server.wait_for_termination()

def forward_request_to_slave(servicer_instance, node, method, *args):
    try:
        with grpc.insecure_channel(node) as channel:
            stub = cache_service_pb2_grpc.CacheServiceStub(channel)
            if method == "Get":
                return stub.Get(*args)
            elif method == "Put":
                return stub.Put(*args)
            elif method == "Remove":
                return stub.Remove(*args)
            else:
                print(f"Unknown method '{method}' requested.")
                return None  # Consider using a default response indicating method error
    except grpc.RpcError as e:
        print(f"RPC error communicating with node {node}. Status: {e.code()}. Details: {e.details()}.")
        # If it's a connection error, consider deregistering the node
        if e.code() == grpc.StatusCode.UNAVAILABLE:
            print(f"Deregistering node {node} due to communication error.")
            ip, port = node.split(":")
            deregister_request = NodeInfo(ip=ip, port=port)
            servicer_instance.DeregisterNode(deregister_request, None)
        return None
    except Exception as e:
        print(f"Unexpected error communicating with node {node}: {e}")
        return None
        
def register_with_master(master_node, slave_ip, slave_port):
    print (f"Registering with master node {master_node}")
    with grpc.insecure_channel(master_node) as channel:
        stub = cache_service_pb2_grpc.CacheServiceStub(channel)
        response = stub.RegisterNode(NodeInfo(ip=slave_ip, port=slave_port))
        print(response.message)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Distributed Cache Server")
    parser.add_argument("node_type", choices=["master", "slave"], help="Type of the node ('master' or 'slave')")
    parser.add_argument("port", default=50051, type=int, help="Port number to start the node on")
    parser.add_argument("--master_ip", default="localhost", help="IP address of the master node (required if node_type is 'slave')")
    parser.add_argument("--master_port", type=int, default=50051, help="Port number of the master node (required if node_type is 'slave')")
    parser.add_argument("--service_name", default="localhost", help="Docker Compose service name for the slave node (optional)")

    args = parser.parse_args()

    ip_address = socket.gethostbyname(socket.gethostname())

    if args.node_type == "master":
        serve(is_master=True, port=args.port)
    elif args.node_type == "slave":
        service_name = args.service_name if args.service_name != "localhost" else ip_address
        register_with_master(f"{args.master_ip}:{args.master_port}", service_name, args.port)
        serve(is_master=False, port=args.port)
    else:
        print("Unknown node type. Use 'master' or 'slave'.")