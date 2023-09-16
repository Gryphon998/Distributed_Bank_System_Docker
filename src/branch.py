# coding:utf-8
import grpc
import time
import message_pb2 as pb2
import message_pb2_grpc as pb2_grpc
from grpc_reflection.v1alpha import reflection
import pymongo
from concurrent import futures
from grpc_reflection.v1alpha import reflection


class Branch(pb2_grpc.BankServiceServicer):

    def __init__(self, id, balance):
        # unique ID of the branch
        self.id = id
        # balance of this branch
        self.balance = balance
        # the bind address for this branch
        self.bind_address = None
        # the list of client stubs to communicate with this branch
        self.stubList = list()
        # set initial logical clock as 0
        self.clock = 0
        # branch logger to store this branch's activities
        self.branch_logger = None
        # event logger to store the events between this branch and its customers
        self.event_logger = None

        self.mongodb_init()

    def mongodb_init(self):
        server_client = pymongo.MongoClient(host='localhost', port=27017)
        server_db = server_client['server_database']
        self.clock_map = server_db['clock_map']
        clock = {'clock': 1}
        self.clock_map.insert_one(clock)

    def MsgDelivery(self, request, context):
        if request.interface == "deposit":
            money = request.money + self.balance
            result = self.clock_map.find({'clock': {'$exists': True}})
            for doc in result:
                local_clock = doc['clock']
            new_clock = max(request.clock + 1, local_clock)
            update_clock = {'_id': doc['_id']}
            self.clock_map.update_one(update_clock, {'$set': {'clock': new_clock}})
            result = "hello, " + request.interface + str(request.money)
            print(result)
            return pb2.MsgDeliveryReply(interface="deposit", result=result, money=money, clock=new_clock)


def serve():
    port = "50001"
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    pb2_grpc.add_BankServiceServicer_to_server(Branch(1, 200), server)
    server.add_insecure_port("[::]:" + port)
    server.start()
    print("Server started, listening on " + port)
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
