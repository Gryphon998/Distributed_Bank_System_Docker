# Distributed_Bank_System_Docker
This project is based on BreadcrumbsCSE531_Lamport_Logical_Clock, with docker container to simulate mutiple bank branches and users, and mongoDB to save local clock.

## Dockerfile and dependencies
Building Python image

```
FROM python:3.10

WORKDIR ./docker_demo

ADD . .

RUN pip install --upgrade pip
RUN pip install --upgrade setuptools
RUN pip install -r requirements.txt
```
requirements.txt file :
```
grpcio==1.57.0
grpcio-reflection==1.57.0
grpcio-tools==1.57.0
protobuf==4.24.1
pymongo==4.5.0
```

## Docker-compose file
Included mangooDB (for both customers and bank branches) containers and clients/bank branches containers
```
services:
  client_mongo:
    image: mongo:latest
    container_name: client_mongo
    ports:
      - "27017:27017"
    volumes:
      - client_mongo_data:/data/db

  service_mongo:
    image: mongo:latest
    container_name: service_mongo
    ports:
      - "27018:27017"
    volumes:
      - service_mongo_data:/data/db

  client:
    image: demo:v1
    command: python src/client.py
    network_mode: "host"
    depends_on:
      - service
      - client_mongo
    environment:
      MONGO_URI: mongodb://client_mongo:27017/mydatabase

  service:
    image: demo:v1
    command: python src/branch.py
    network_mode: "host"
    depends_on:
      - service_mongo
    environment:
      MONGO_URI: mongodb://service_mongo:27017/mydatabase

volumes:
  client_mongo_data:
  service_mongo_data:
```

## Proto file
```
syntax = "proto3";

package bank;

service BankService {
    rpc MsgDelivery (MsgDeliveryRequest) returns (MsgDeliveryReply){}
}

message MsgDeliveryRequest {
    sint64 id = 1;
    string interface = 2;
    int64 money = 3;
    int64 clock = 4;
}

message MsgDeliveryReply {
    string interface = 1;
    string result = 2;
    int64 money = 3;
    int64 clock = 4;
}
```
