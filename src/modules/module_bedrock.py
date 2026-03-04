import requests

import boto3
import json
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest

from modules.module_messageQue import queue_message
from modules.module_config import load_config

CONFIG = load_config()
class BedrockService():
    def __init__(self):
        self.model = CONFIG["LLM"]["bedrock_model"]
        self.region = CONFIG["LLM"]["aws_default_region"]
        self.url = CONFIG["LLM"]["bedrock_url"].format(region = self.region, model=self.model)
        self.credentials = boto3.Session().get_credentials()
        
    
    def _sign_request(self, payload: dict) -> dict:
        body = json.dumps(payload)
        request = AWSRequest(method="POST", url=self.url, data=body, headers={"Content-Type": "application/json"})
        SigV4Auth(self.credentials, "bedrock", self.region).add_auth(request)
        return dict(request.headers)
    
    def make_request(self, payload) -> str:
        headers = self._sign_request(payload)
        response = requests.post(self.url, json=payload, headers=headers)
        return response