from concurrent import futures
import grpc
from app.serve.calls import GreetService
from app.serve import greet_pb2_grpc


server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
greet_pb2_grpc.add_GreetServiceServicer_to_server(GreetService(), server)
print("Starting server at 5000...")
server.add_insecure_port("[::]:50051")
server.start()
server.wait_for_termination()
