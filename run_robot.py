# -*- coding:utf-8 -*-

from QA import Dialog_system


if __name__ == "__main__":
    dialog_system = Dialog_system()
    while True:
        q = input(':: ')
        if q == 'exit' or q == 'stop' or q == 'quit' or q == 'q':
            break
        else:
            # 如果用户输入空字符串，不作回复
            # 如果用户输入有效字符串，首先通过 bot(闲聊问答逻辑)搜索回答
            # 如果闲聊逻辑返回空回答，则同时搜索语料库和调用搜索引擎，并通过 net(神经网络模型)计算各个回答的匹配度
            # 最后返回匹配度最高的回答
            if not q:
                continue
            answer = dialog_system.response(q)
            print('>>', answer)