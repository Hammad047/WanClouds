import json
from app import app, api
from database.db import db
from app.serve import greet_pb2, greet_pb2_grpc


class GreetService(greet_pb2_grpc.GreetServiceServicer):
    def Greet(self, request, context):
        with app.app_context():
            response = greet_pb2.GreetResponse()
            results = db.session.query(api.Car).filter_by(object_id=request.object_id).first()
            response.data = json.dumps(results.display())
            response.status = "202"
            return response
