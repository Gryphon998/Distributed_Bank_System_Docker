import grpc
import message_pb2 as pb2
import message_pb2_grpc as pb2_grpc
import pymongo
from concurrent import futures


class Branch(pb2_grpc.BankServiceServicer):

    def __init__(self, id, balance):
        # unique ID of the branch
        self.id = id
        # balance of this branch
        self.balance = balance
        # set initial logical clock as 0
        self.clock = 0
        # init the mongoDB database
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
            # Using Lamport clock algorithm to compare local clock and received clock
            new_clock = max(request.clock + 1, local_clock)
            update_clock = {'_id': doc['_id']}
            # Update local clock
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
