from __future__ import print_function

import logging
import pymongo

import grpc
import message_pb2_grpc
import message_pb2


def run():
    print("Will try to send message")
    with grpc.insecure_channel("localhost:50001") as channel:
        client = pymongo.MongoClient(host='localhost', port=27017)
        db = client['database']
        clock_map = db['clock_map']
        clock = {'clock': 1}
        clock_map.insert_one(clock)
        stub = message_pb2_grpc.BankServiceStub(channel)
        response = stub.MsgDelivery(message_pb2.MsgDeliveryRequest(id=1, interface="deposit", money=200, clock=1))
        clock_map.update_one(clock, {'$set': {'clock': response.clock}})
    print("Greeter client received: " + str(response))


if __name__ == "__main__":
    logging.basicConfig()
    run()
