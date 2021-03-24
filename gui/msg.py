import json
import time
import stomp


class OnMsg(stomp.ConnectionListener):

    def __init__(self, decoder):
        self.decoder = decoder

    def on_message(self, headers, body):
        # print(body)
        self.decoder.set_last_msg(body)


class MessageDispatcher:

    def __init__(self):
        self._last_msg = {'time_stamp': 0}
        self._conn = stomp.Connection([('127.0.0.1', 61613)])
        self._conn.set_listener('render_client_listener', OnMsg(self))
        # self._conn.start()
        self._conn.connect()
        self._conn.subscribe('/topic/PhysicsWorldInfoTopic', 'render_client')

    def close(self):
        self._conn.disconnect()

    def set_last_msg(self, msg):
        data = json.loads(msg)
        if int(data['time_stamp']) > int(self._last_msg['time_stamp']):
            self._last_msg = data

    def pull_msg(self):
        while self._last_msg['time_stamp'] == 0:
            print('Waiting for server...')
            time.sleep(1)
        return self._last_msg
