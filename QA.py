# -*- coding: utf-8 -*-
"""
Created on Sat May 12 13:57:55 2018

@author: hasee
"""

from modules.main import Chatter
from modules.nn import QA_LSTM_net
import requests
import json
import operator

class Dialog_system():
    
    def __init__(self):
        self.bot = Chatter()
        self.net = QA_LSTM_net()
        self.net.restore()
        self.net.restore_embed()
        self.net.set_eval()
    
    def response(self, q):
        answer = self.bot.search_answer(q)
        if answer:
            return answer
        answer_cand = {}
        sub_answer, sub_score = self.net.forward(q)
        answer_cand[sub_answer] = sub_score
        # response = requests.get('http://111.230.235.183:5000/qaByBd/' + q)
        # response_dict = json.loads(response.text)
        # if type(response_dict['data']) == str:
        #     sub_answer = response_dict['data'].strip()
        #     sub_score = self.net.cal_confidence(q, sub_answer)
        #     answer_cand[sub_answer] = sub_score
        # else:
        #     for sub_dict in response_dict['data']:
        #         for key in sub_dict:
        #             sub_answer = sub_dict[key].strip()
        #             sub_score = self.net.cal_confidence(q, sub_answer)
        #             answer_cand[sub_answer] = sub_score
        sorted_answer = sorted(answer_cand.items(), key = operator.itemgetter(1), reverse = True)
        answer = sorted_answer[0][0]
        return answer