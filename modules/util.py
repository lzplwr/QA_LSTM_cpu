# -*- coding: utf-8 -*-
"""
Created on Tue Mar 13 17:24:46 2018

@author: hasee
"""

import xlrd
import os

code_path = os.path.realpath(__file__)
dir_path = os.path.dirname(os.path.dirname(code_path))

# 读取语料库的函数 read_table

def read_table(file_name):
    file_path = os.path.join(dir_path, 'data', file_name)
    data = xlrd.open_workbook(file_path)
    table = data.sheets()[0]
    questions = table.col_values(0)
    answers = table.col_values(1)
    data_pairs = [ (questions[i],answers[i]) for i in range(len(questions)) ]
    data_pairs = [ (str(q).strip(),str(a).strip()) for (q,a) in data_pairs if q and a ]
    return data_pairs

def read_hi_table(file_name):
    file_path = os.path.join(dir_path, 'data', file_name)
    data = xlrd.open_workbook(file_path)
    table_hi = data.sheets()[0]
    table_revise = data.sheets()[1]
    questions_hi = table_hi.col_values(0)
    answers_hi = table_hi.col_values(1)
    questions_revise = table_revise.col_values(0)
    answers_revise = table_revise.col_values(1)
    data_pairs_hi = [(questions_hi[i], answers_hi[i]) for i in range(len(questions_hi))]
    data_pairs_revise = [ (questions_revise[i],answers_revise[i]) for i in range(len(questions_revise)) ]
    data_pairs = data_pairs_hi + data_pairs_revise
    data_pairs = [ (str(q).strip(),str(a).strip()) for (q,a) in data_pairs if q and a ]
    return data_pairs

# 读取验证集和测试集的 read_test_table

def read_test_table(file_name):
    file_path = os.path.join(dir_path, 'data', file_name)
    data = xlrd.open_workbook(file_path)
    table = data.sheets()[0]
    questions = table.col_values(0)
    pos_answers = table.col_values(1)
    neg_answers = table.col_values(2)
    data_pairs = [ (questions[i],pos_answers[i],neg_answers[i]) for i in range(len(questions)) ]
    data_pairs = [ (str(q).strip(),str(p).strip(),str(n).strip()) for (q,p,n) in data_pairs if q and p and n ]
    return data_pairs

def read_answer():
    data = read_table('corpus.xlsx')
    answers = [ a for (q,a) in data ]
    return answers

def read_question():
    data = read_table('corpus.xlsx')
    questions = [ q for (q,a) in data ]
    return questions