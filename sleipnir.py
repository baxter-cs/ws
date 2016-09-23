###############################################################################
#
# The MIT License (MIT)
#
# Copyright (c) Tavendo GmbH | Modified by JCharante
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
###############################################################################

# This example shows you running a autobahn|python server & client in the same script
# In order to run it first install the dependencies
# sudo apt install python3 python3-dev
# pip install autobahn[twisted]
# and then run this example.

from autobahn.twisted.websocket import WebSocketServerProtocol, WebSocketServerFactory, WebSocketClientProtocol, WebSocketClientFactory
import json
import js


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


class MyClientProtocol(WebSocketClientProtocol):

    def printf(self, message):
        print("Client   |", message)

    def onConnect(self, response):
        self.printf("Server connected: {0}".format(response.peer))

    def send_text(self, message):
        self.sendMessage(message.encode('UTF-8'), False)

    def send_JSON(self, dictionary):
        self.sendMessage(json.dumps(dictionary).encode('UTF-8'), False)

    def onOpen(self):
        self.printf("WebSocket connection open.")

        self.send_JSON({
            'data': 'rawr',
            'gid': '2iji2jdi2j'
        })

    def onMessage(self, payload, isBinary):
        if isBinary:
            self.printf("Binary message received: {0} bytes".format(len(payload)))
        else:
            message = decode_json(payload)
            if message[0]:
                message = message[1]
                self.printf("Received message from Sleipnir: {}".format(message))
            else:
                message = decode_text(payload)
                self.printf("Couldn't decode json from this message: {}".format(message))
                self.send_JSON({
                    'success': False,
                    'type': 'Error message',
                    'data': 'json not detected in your message'
                })

    def onClose(self, wasClean, code, reason):
        self.printf("WebSocket connection closed: {0}".format(reason))


class MyServerProtocol(WebSocketServerProtocol):

    def __init__(self):
        super().__init__()
        self.gid = None

    def printf(self, message):
        print("Sleipnir |", message)

    def onConnect(self, request):
        self.printf("Client connecting: {}".format(request.peer))

    def onOpen(self):
        self.printf("WebSocket connection open.")
        self.send_text("Connected... Please send over your gid")

    def onMessage(self, payload, isBinary):
        response = dict()
        if isBinary:
           self.printf("Binary message received: {} bytes".format(len(payload)))
        else:
            message = decode_json(payload)
            if message[0]:
                message = message[1]
                if self.gid is None:
                    self.gid = message.get('gid', None)
                    self.send_JSON({
                        'success': self.gid is not None,
                        'data': 'thank you for sending your gid' if self.gid is not None else 'please send your gid'
                    })
                else:
                    self.printf("Received message from client: {}".format(message))
                    self.send_JSON({
                        'gid': self.gid,
                        'success': True
                    })
            else:
                message = self.decode_text(payload)
                self.printf("Couldn't decode json from this message: {}".format(message))
                self.send_JSON({
                    'success': False,
                    'type': 'Error message',
                    'data': 'json not detected in your message'
                })

    def send_text(self, message):
        self.sendMessage(message.encode('UTF-8'), False)

    def send_JSON(self, dictionary):
        self.sendMessage(json.dumps(dictionary).encode('UTF-8'), False)

    def onClose(self, wasClean, code, reason):
        self.printf("WebSocket connection closed: {}".format(reason))

if __name__ == '__main__':

    import sys

    from twisted.python import log
    from twisted.internet import reactor

    log.startLogging(sys.stdout)

    #factory = WebSocketServerFactory(u"ws://127.0.0.1:9000")
    #factory.protocol = MyServerProtocol
    # factory.setProtocolOptions(maxConnections=2)

    #reactor.listenTCP(9000, factory)
    #reactor.run()

    a = js.WServerHandler()
    a.start(True)

    #f = WebSocketClientFactory(u"ws://127.0.0.1:9000")
    #f.protocol = MyClientProtocol

    #reactor.connectTCP("localhost", 9000, f)
    #reactor.run()

