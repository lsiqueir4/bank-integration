import json
import time
import requests
import base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec
from flask import current_app


class StarkConnector:
    def __init__(self):
        self.accessId = "project/6299291431731200"
        self.base_url = "https://sandbox.api.starkbank.com/v2"

    def create_signature(self, body_string):
        message = (
            self.accessId + ":" + str(int(time.time())) + ":" + body_string
        ).encode()

        with open("privateKey.pem", "rb") as f:
            private_key = serialization.load_pem_private_key(f.read(), password=None)

        signature = private_key.sign(message, ec.ECDSA(hashes.SHA256()))
        access_signature = base64.b64encode(signature).decode()

        return access_signature

    def do_request(self, payload: dict, method: str, url: str):
        accessTime = str(int(time.time()))
        body_string = json.dumps(payload)
        access_signature = self.create_signature(body_string)

        current_app.logger.info(
            f"Making {method} request to {self.base_url + url} with payload: {payload}"
        )
        request = requests.request(
            url=self.base_url + url,
            json=payload,
            method=method,
            headers={
                "Access-Id": self.accessId,
                "Access-Time": accessTime,
                "Access-Signature": access_signature,
            },
        )
        current_app.logger.info(
            f"Received response: {request.status_code} {request.text}"
        )
        return request.json()

    def create_invoices(self, payload):
        return self.do_request(payload, "POST", "/invoice")
