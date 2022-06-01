import hashlib
import hmac
import base64
import time
import requests
import json
import pprint


class ChatbotMessageSender:
    # 챗봇 `api 게이트웨이 url
    ep_path = 'https://jyiq09glzg.apigw.ntruss.com/custom/v1/6976/3d3d2b9a198af4364d5947f54d8777186f35511e9a6110e6b1759696b14a9891'
    # 챗봇 secret key
    secret_key = 'd29WQ0VnR3J1bEhvempvRGVKVkVWSWRDSkVOUmhPTVc='

    # 사용자 메시지 전송
    def req_message_send(self, question):
        # html post형식으로 데이터 받아오기
        timestamp = self.get_timestamp()
        request_body = {
            'version': 'v2',
            'userId': 'U47b00b58c90f8e47428af8b7bddcda3d1111111',
            'timestamp': timestamp,
            'bubbles': [
                {
                    'type': 'text',
                    'data': {
                        'description': question
                    }
                }
            ],
            'event': 'send'
        }

        ## Request body(클로바 챗봇에 맞게 인코딩)
        encode_request_body = json.dumps(request_body).encode('UTF-8')

        ## make signature
        signature = self.make_signature(self.secret_key, encode_request_body)

        ## headers
        custom_headers = {
            'Content-Type': 'application/json;UTF-8',
            'X-NCP-CHATBOT_SIGNATURE': signature
        }

        """
        print("## Timestamp : ", timestamp)
        print("## Signature : ", signature)
        print("## headers ", custom_headers)
        print("## Request Body : ", encode_request_body)
        """

        ## POST Request(POST 요청, data에 있는 정보를 POST로 전송)
        response = requests.post(headers=custom_headers, url=self.ep_path, data=encode_request_body)

        return response

    @staticmethod
    def get_timestamp():
        timestamp = int(time.time() * 1000)
        return timestamp

    @staticmethod
    def make_signature(secret_key, request_body):
        secret_key_bytes = bytes(secret_key, 'UTF-8')

        signing_key = base64.b64encode(hmac.new(secret_key_bytes, request_body, digestmod=hashlib.sha256).digest())

        return signing_key
# def json_parsing(qwe):
#     json_data = json.loads(qwe.text)
#     result = json_data['bubbles'][0]['data']['description']
#     return result

def json_parsing(qwe):
    json_data = json.loads(qwe.text)
    # result = json_data['bubbles'][0]['data']['description']
    #질문 답변 타입
    # json_data['bubbles'][0]['type']
    # print(json_data['bubbles'][0]['type'])
    return json_data

if __name__ == '__main__':

    res = ChatbotMessageSender().req_message_send('빨래하고 싶어')
    # a = json_parsing(res)
    a = json_parsing(res)
    print(res.text)
    # if (res.status_code == 200):
    #     pprint.pprint(res.text)
        # print(res.read().decode("UTF-8"))