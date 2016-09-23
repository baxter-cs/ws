# JCharante's Socket Layer

from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory, WebSocketClientProtocol, WebSocketClientFactory
import json

from twisted.python import log
from twisted.internet import reactor


def is_json(payload):
    try:
        json.loads(payload.decode('utf8'))
        return True
    except:
        return False


def decode_text(payload):
    return payload.decode('utf8')


def decode_json(payload):
    try:
        return [True, json.loads(payload.decode('utf8'))]
    except:
        return [False, {}]


class BaseClient(WebSocketClientProtocol):

    def __init__(self):
        super().__init__()

    def onConnect(self, response):
        pass

    def send_text(self, message):
        self.sendMessage(message.encode('UTF-8'), False)

    def send_JSON(self, dictionary):
        self.sendMessage(json.dumps(dictionary).encode('UTF-8'), False)

    def onOpen(self):
        pass

    def onMessage(self, payload, isBinary):
        if isBinary:
            pass
        else:
            pass

    def onClose(self, wasClean, code, reason):
        pass


class BaseServer(WebSocketServerProtocol):

    def __init__(self):
        super().__init__()

    def printf(self, message):
        print(message)

    def onConnect(self, request):
        self.printf("Client connecting: {}".format(request.peer))

    def onOpen(self):
        pass

    def onMessage(self, payload, isBinary):
        if isBinary:
           pass
        else:
            pass

    def send_text(self, message):
        self.sendMessage(message.encode('UTF-8'), False)

    def send_JSON(self, dictionary):
        self.sendMessage(json.dumps(dictionary).encode('UTF-8'), False)

    def onClose(self, wasClean, code, reason):
        pass


class WServer(BaseServer):

    def __init__(self):
        super().__init__()
        self.nickname = 'Sleipnir'

    def printf(self, message):
        print('{} | {}'.format(self.nickname, message))


class FakeIRC(BaseServer):

    def __init__(self):
        super().__init__()
        self.nickname = 'FakeIRC'


class WServerHandler:

    def __init__(self, address=u"ws://127.0.0.1:1337", port=1337, nickname='Sleipnir'):
        super().__init__()
        self.address = address
        self.port = port

    def start(self, lock=False):
        factory = WebSocketServerFactory(self.address)
        factory.protocol = WServer
        # factory.setProtocolOptions(maxConnections=2)

        reactor.listenTCP(self.port, factory)
        if lock:
            reactor.run()
