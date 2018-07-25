# -*- coding: utf-8 -*-
"""
Created on Tue Mar 13 17:19:53 2018

@author: hasee
"""

from modules.main import Chatter
from modules.nn import QA_LSTM_net
import requests
import json
import operator
import os
import readline
from flask import Flask,jsonify,request

bot = Chatter()

net = QA_LSTM_net()
net.restore()
net.set_eval()

code_path = os.path.realpath(__file__)
dir_path = os.path.dirname(code_path)
file_path = os.path.join(dir_path,'log','dialog_record.txt')


app = Flask(__name__)

@app.route("/api",methods=['POST'])
def index():
	question=request.form.get('sentence','')
	print("question: ", question)
	print("--------------------------")
	print(request.form.get("question"))
	answer = chat(question)
	print(answer)
	return jsonify({'result': answer, 'status': 'success'})

def chat(question):
	answer = bot.search_answer(question)
	print("闲聊模块: ", answer)
	if not answer:
		answer_cand = {}
		# 获取语料库中匹配度最高的答案
		sub_answer, sub_score = net.forward(question)
		answer_cand[sub_answer] = sub_score
		# 获取搜索引擎返回的答案，并计算它们的匹配度
			# response = requests.get('http://127.0.0.1:9009/qaByBd/' + question)
			# response_dict = json.loads(response.text)
			# print(response_dict)
			# if type(response_dict['data']) == str:
			# 	sub_answer = response_dict['data'].strip()
			# 	sub_score = net.cal_confidence(question, sub_answer)
			# 	answer_cand[sub_answer] = sub_score
			# else:
			# 	for sub_dict in response_dict['data']:
			# 		for key in sub_dict:
			# 			sub_answer = sub_dict[key].strip()
			# 			sub_score = net.cal_confidence(question, sub_answer)
			# 			answer_cand[sub_answer] = sub_score
		sorted_answer = sorted(answer_cand.items(), key = operator.itemgetter(1), reverse = True)
		answer = sorted_answer[0][0]
	return answer

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=9008,debug =True)