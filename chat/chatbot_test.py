from chat import chatbot_config
if __name__ == '__main__':

    res = chatbot_config.ChatbotMessageSender().req_message_send('동아리가 궁금해')
    chat_message = chatbot_config.json_parsing(res)

    if (res.status_code == 200):
        print(chat_message)
        # print(res.read().decode("UTF-8"))