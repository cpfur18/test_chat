from chat import chatbot_config
if __name__ == '__main__':

    res = chatbot_config.ChatbotMessageSender().req_message_send('안녕')

    print(res.status_code)
    if (res.status_code == 200):
        print(res.text)
        # print(res.read().decode("UTF-8"))