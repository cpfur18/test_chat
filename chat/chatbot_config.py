import hashlib
import hmac
import base64
import time
import requests
import json
import pprint


class ChatbotMessageSender:
    # 챗봇 `api 게이트웨이 url
    ep_path = 'https://9kacj920ed.apigw.ntruss.com/custom/v1/7036/2e26ad07493b674c401b4d331820df08b05b6f8d6eb935c6463bb3e9bfdcfeda'
    # 챗봇 secret key
    secret_key = 'cUJmb1VpVWJ0RFBQTnBud1BDblZwaGlCb1J2b3dPTEs='

    # 웰컴 메시지
    def req_message_open(self, question):
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
            'event': 'open'
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

# def json_parsing2(question):
#     json_data = json.loads(question.text)
#     print(json_data)
#     count_contentTable = len(json_data['bubbles'][0]['data']['contentTable'])
#     print(json_data['bubbles'][0]['data']['contentTable'][0][0])
#     for i in range(count_contentTable):
#         print(i)
#         title = json_data['bubbles'][0]['data']['contentTable'][0]['data']['title']
#         displayText = json_data['bubbles'][0]['data']['contentTable'][i]['data'].get('displayText')
#         postbackFull = json_data['bubbles'][0]['data']['contentTable'][i]['data'].get('postbackFull')
#
#         locals()['contentTable' + str(i)] = json.dumps({
#                 'title': title,
#                 'displayText': displayText,
#                 'postbackFull': postbackFull,
#         })
#         print(contentTable[i])

# def template_image_send(self, res):
#     json_data = json.loads(res.text)
#     title = json_data['bubbles'][0]['data'].get('title')
#     count_contentTable = len(json_data['bubbles'][0]['data']['contentTable'][0][0])
#     subTitle = json_data['bubbles'][0]['data']['subTitle']
#     description = json_data['bubbles'][0]['data']['data']['description']
#     url = json_data['bubbles'][0]['data']['data']['url']
#     urlAlias = json_data['bubbles'][0]['data']['data']['urlAlias']


if __name__ == '__main__':
    res = ChatbotMessageSender().req_message_send('동서대 편의시설')
    json_data = json.loads(res.text)
    response = json_data['bubbles'][0]
    print(response)



