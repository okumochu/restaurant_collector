import tiktoken


def num_tokens_from_messages(messages, model='gpt-3.5-turbo'):
    encoding = tiktoken.encoding_for_model(model)
    num_tokens = 0
    for message in messages:
        # every message follows <im_start>{role/name}\n{content}<im_end>\n
        num_tokens += 4
        for key, value in message.items():
            num_tokens += len(encoding.encode(value))
            if key == "name":  # if there's a name, the role is omitted
                num_tokens += -1  # role is always required and always 1 token
    num_tokens += 2  # every reply is primed with <im_start>assistant
    return num_tokens


def article_to_GPT(list_of_articles, start_index):
    token_limit = 3500
    sentence_token = len(max(list_of_articles, key=len))*3
    # print(max(list_of_articles))
    # print(sentence_token)
    a = list_of_articles
    index = start_index
    message = []
    message_token = 0
    # print('first step')
    while True:
        for _ in range((token_limit-message_token)//sentence_token):
            if index < len(a):
                message.append(
                    {"role": "user", "content": str(a[index])})
                index += 1
            else:
                # print(message)
                # print()
                print(num_tokens_from_messages(message))
                return message, index

        message_token = num_tokens_from_messages(message)
        # print(token_limit - message_token)
        if (token_limit-message_token)//sentence_token <= 0:
            # print(message)
            # print()
            print(num_tokens_from_messages(message))
            return message, index
