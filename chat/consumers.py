import json
from channels.generic.websocket import WebsocketConsumer
from chat import chatbot_config

# if __name__ == '__main__':
#
#     res = chatbot_config.ChatbotMessageSender().req_message_send('안녕')
#
#     print(res.status_code)
#     if (res.status_code == 200):
#         print(res.text)
#         # print(res.read().decode("UTF-8"))

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, close_code):
        pass

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        # print(text_data_json)
        message = text_data_json['message']
        # print(message)
        res = chatbot_config.ChatbotMessageSender().req_message_send(message)
        qwe = chatbot_config.json_parsing(res)
        self.send(text_data=json.dumps({
            'message': qwe
        }))