from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
from threading import Thread
from cryptography.fernet import Fernet
import json
import time


secret_key = 'SkgGFenksd7qpNSbpRbQgHEZmenze5LIkH0tUoppBKg='

fern = Fernet(secret_key)


class ChatProto(DatagramProtocol):

    def __init__(self, name):
        self.name = name

    def startProtocol(self):
        self.transport.setTTL(5)
        self.transport.joinGroup("228.0.0.5")

    def datagramReceived(self, datagram, address):
        data = json.loads(fern.decrypt(datagram).decode('utf-8'))
        if data['name'] != self.name:
            print("[%s]: %s" % (data['name'], data['msg']))

    def send(self, msg):
        data = {
            'name': self.name,
            'msg': msg,
            'data': time.strftime('%H:%M:%S')
        }
        self.transport.write(fern.encrypt(json.dumps(data).encode('utf-8')), ("228.0.0.5", 8005))


class Input(Thread):

    def __init__(self):
        super().__init__(target=self.run)
        self.start()

    def run(self):
        while True:
            proto.send(input())


proto = ChatProto(input('Enter your name:\n'))
print('---- CHAT ----')
inp = Input()
reactor.listenMulticast(8005, proto,
                        listenMultiple=True)
reactor.run()
