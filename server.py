'''
################################## server.py #############################
# Lab1 gRPC RocksDB Server 
################################## server.py #############################
'''
import time
import grpc
import datastore_pb2
import datastore_pb2_grpc
import uuid
import rocksdb

from concurrent import futures

_ONE_DAY_IN_SECONDS = 60 * 60 * 24

class MyDatastoreServicer(datastore_pb2.DatastoreServicer):
    def __init__(self):
        self.db = rocksdb.DB("lab1.db", rocksdb.Options(create_if_missing=True))

    def put(self, request, context):
        print("put")
        key = uuid.uuid4().hex
        # save to db
        value = request.data.encode()  # encode request data to bytes
        self.db.put(b"key", value)

        return datastore_pb2.Response(data=key)

    def get(self, request, context):
        print("get")
         
        key = request.data # get incoming request data
        value = self.db.get(b'key').decode("utf-8")
        return datastore_pb2.Response(data=value)

def run(host, port):
    '''
    Run the GRPC server
    '''
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=1))
    datastore_pb2_grpc.add_DatastoreServicer_to_server(MyDatastoreServicer(), server)
    server.add_insecure_port('%s:%d' % (host, port))
    server.start()

    try:
        while True:
            print("Server started at...%d" % port)
            time.sleep(_ONE_DAY_IN_SECONDS)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    run('0.0.0.0', 3000)
