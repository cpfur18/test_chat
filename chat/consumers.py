import json
from channels.generic.websocket import WebsocketConsumer
from . import chatbot_config
from . import json_parser
from time import sleep

class MessageSender(WebsocketConsumer):
    check = json_parser.JsonCheck()

    # 텍스트 타입
    def text_send(self, res):
        json_data = json.loads(res.text)
        message = self.check.text_full_check(json_data)

        # 텍스트 스타일 체크
        if message == True:
            description = json_data['bubbles'][0]['data'].get('description')
            url = json_data['bubbles'][0]['data'].get('url')
            urlalias = json_data['bubbles'][0]['data'].get('urlAlias')
            json_string = json.dumps({
                'case': 'full_text',
                'type': 'text',
                'description': description,
                'url': url,
                'urlAlias': urlalias,
            })
        else:

            description = json_data['bubbles'][0]['data'].get('description')
            json_string = json.dumps({
                'case': 'text',
                'type': 'text',
                'style': False,
                'description': description,
            })
        return json_string

    # 이미지 타입
    def image_send(self, res):
        json_data = json.loads(res.text)
        message = self.check.img_full_check(res)

        # 이미지 스타일 체크
        if message == True:
            title = json_data['bubbles'][0]['title']
            subTitle = json_data['bubbles'][0]['subTitle']
            imageUrl = json_data['bubbles'][0]['data']['imageUrl']
            imagePosition = json_data['bubbles'][0]['data']['imagePosition']
            description = json_data['bubbles'][0]['data']['description']
            url = json_data['bubbles'][0]['data']['action']['data']['url']
            json_string = json.dumps({
                'title': title,
                'subTitle': subTitle,
                'imageUrl': imageUrl,
                'imagePosition': imagePosition,
                'description': description,
                'url': url,
            }, ensure_ascii=False)
        else:
            imageUrl = ['bubbles'][0]['data']['imageUrl']
            imagePosition = ['bubbles'][0]['data']['imagePosition']
            description = json_data['bubbles'][0]['data']['description']
            json_string = json.dumps({
                'type': 'image',
                'imageUrl': imageUrl,
                'imagePosition': imagePosition,
                'description': description,
            }, ensure_ascii=False)
        return json_string

    # 템플릿 형식 답변 텍스트 + 버튼
    def template_text_send(self, res):
        json_data = json.loads(res.text)
        count_contentTable = len(json_data['bubbles'][0]['data']['contentTable'][0])

        json_data['case'] = 'text_template'
        json_data['count'] = count_contentTable

        json_string = json.dumps(json_data, ensure_ascii=False)

        return json_string
    # 템플릿 형식 답변 이미지 + 버튼
    def template_image_send(self, res):
        json_data = json.loads(res.text)
        count_contentTable = len(json_data['bubbles'][0]['data']['contentTable'][0])
        json_data['case'] = 'image_template'
        json_data['count'] = count_contentTable

        json_string = json.dumps(json_data, ensure_ascii=False)

        return json_string

    # # 템플릿 형식 답변 이미지 리스트
    # def template_imagelist_send(self, res):


class ChatConsumer(WebsocketConsumer):
    # 웹 소켓 연결
    def connect(self):
        self.accept()

    # 웹 소켓 연결 해제
    def disconnect(self, close_code):
        pass

    # HTML에서 rqs 신호 받을 시 행동
    def receive(self, text_data):
        text_data_json = json.loads(text_data)

        # HTML 문서 rqs 신호 변수에 저장
        message = text_data_json['message']

        # 클래스 변수 선언
        send_chatbot = chatbot_config.ChatbotMessageSender()
        send_message = MessageSender()
        check = json_parser.JsonCheck()

        # 챗봇 Json 형태 응답
        res = send_chatbot.req_message_send(message)

        # 오픈 메시지 유무 체크
        if message == "postback text of welcome action":
            res = send_chatbot.req_message_open(message)
            self.send(text_data=send_message.text_send(res))
        else:
            message = check.template_check(res)
            # 템플릿 타입 체크
            if message == False:
                print('Not 템플릿')

                message = check.text_check(res)
                # 텍스트 타입 체크
                if message == True:
                    print('Yes 텍스트')
                    self.send(text_data=send_message.text_send(res))
                else:
                    message = check.img_check(res)
                    # 이미지 타입 체크
                    if message == True:
                        self.send(text_data=send_message.image_send(res))
            # 템플릿 타입 답변 True
            else:
                print('Yes 템플릿')
                message = check.template_text_check(res)
                # 템플릿 텍스트 타입 체크
                if message == True:
                    print('Yes 템플릿 텍스트')
                    self.send(text_data=send_message.template_text_send(res))
                else:
                    message = check.template_image_check(res)
                    # 템플릿 이미지 타입 체크
                    if message == True:
                        print('Yes 템플릿 이미지')
                        self.send(text_data=send_message.template_image_send(res))
                    # else:
                    #     message = check.template_imagelist_check(res)
                    #     # 템플릿 이미지 리스트 타입 체크
                    #     if message == True:
                    #         ㅁㄴㅇ
            # else:
            #     message = check.multi_check(res)
            #     # 후속 질문 유무 체크
            #     if message == False:
            #         message = check.template_check(res)
            #         # 템플릿 타입 체크
            #         if message ==  False:
            #             message = check.text_check(res)
            #             # 텍스트 타입 체크
            #             if message == True:
            #                 send.text_send(res)
            #             else:
            #                 message = check.img_check(res)
            #                 # 이미지 타입 체크
            #                 if message == True:
            #                     send.image_send(res)

            # else:
            #     message = check.template_check(res)
            #     # 템플릿 타입 체크
            #     if message == False:
            #         message = check.text_check(res)
            #         # 텍스트 타입 체크
            #         if message == True:
            #             send.text_send(res)
            #         else:
            #             message = check.img_check(res)
            #             # 이미지 타입 체크
            #             if message == True:
            #                 send.image_send(res)



        




