import json
from base64 import b64encode, b64decode


class rabbit_body:
    publish_log: dict

    def __init__(self, publish_log):
        self.publish_log = publish_log

    def encode(self):
        dicc = {"publish_log": self.publish_log}
        return b64encode(json.dumps(dicc).encode())

    @staticmethod
    def decode(encoded):
        dicc = json.loads(b64decode(encoded))
        publish_log = dicc["publish_log"]
        return rabbit_body(publish_log)
