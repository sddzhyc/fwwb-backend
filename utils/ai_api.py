from http import HTTPStatus
from dashscope import Generation
import dashscope
dashscope.api_key = 'sk-afc61e5db6a0476886909c952a0acac8'  # 填入第一步获取的APIKEY

def call_with_stream():
    conversation_history = []  # 用于记录对话历史
    user_input = input("Q:")
    while True:

        if not user_input:
            break

        # 添加用户问题到对话历史
        conversation_history.append({'role': 'user', 'content': user_input})

        # 调用对话生成模型
        responses = Generation.call("qwen-turbo",
                                    messages=conversation_history,
                                    result_format='message',
                                    stream=True,
                                    incremental_output=True)

        full_content = ''  # 用于记录完整的对话内容
        for response in responses:
            if response.status_code == HTTPStatus.OK:
                assistant_response = response.output.choices[0]['message']
                full_content += assistant_response['content'] + '\n'  # 记录对话内容
                # print(assistant_response['content'], end='')
                print("\n一个返回：" + assistant_response['content'], end='')
            else:
                print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
                    response.request_id, response.status_code,
                    response.code, response.message
                ))
        user_input = input("\nQ:")
        conversation_history.append({'role': assistant_response['role'], 'content': full_content})
        # 打印完整的对话内容
        # print('Full conversation:\n' + full_content)

def answer_with_stream(user_input ,conversation_history = [] ):
    # conversation_history = []  # 用于记录对话历史
    # user_input = input("Q:")
    # 添加用户问题到对话历史
    conversation_history.append({'role': 'user', 'content': user_input})
    print("conversation_history:",conversation_history)
    # 调用对话生成模型
    responses = Generation.call("qwen-turbo",
                                messages=conversation_history,
                                result_format='message',
                                stream=True,
                                incremental_output=True)

    full_content = ''  # 用于记录完整的对话内容
    for response in responses:
        if response.status_code == HTTPStatus.OK:
            assistant_response = response.output.choices[0]['message']
            # full_content += assistant_response['content'] + '\n'  # 记录对话内容
            full_content += assistant_response['content']  # 记录对话内容

            print("\n一个返回：" + assistant_response['content'], end='')
            # yield assistant_response['content']
        else:
            print('Request id: %s, Status code: %s, error code: %s, error message: %s' % (
                response.request_id, response.status_code,
                response.code, response.message
            ))
            return 'Request id: %s, Status code: %s, error code: %s, error message: %s' % (
                response.request_id, response.status_code,
                response.code, response.message)
    # yield "end"
    conversation_history.append({'role': assistant_response['role'], 'content': full_content})
    # 打印完整的对话内容
    print('Full conversation:\n' + full_content)
    return full_content


if __name__ == '__main__':
    call_with_stream()