# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 16:41:18 2018

@author: hasee
"""

import torch
from fuzzywuzzy import process
from torch.autograd import Variable
from modules.segment import segment,extract_gram
import modules.util as util
from gensim.models.keyedvectors import KeyedVectors
import numpy as np
from pickle import load
import operator
import os

code_path = os.path.realpath(__file__)
dir_path = os.path.dirname(os.path.dirname(code_path))

nb_hidden = 384

max_ql = 50
max_al = 200
margin = 0.1
drop_rate = 0
num_layers = 3
clip_norm = 5
learning_rate = 0.001

min_idf = 4
candicate_num = 100

class RNN(torch.nn.Module):
    
    def __init__(self, nb_hidden, embed_size):
        super(RNN,self).__init__()
        self.hidden_size = nb_hidden
        self.rnn = torch.nn.LSTM(input_size = embed_size, hidden_size = self.hidden_size, num_layers = \
                                 num_layers, batch_first = True, dropout = drop_rate, bidirectional = True)
        
    def forward(self,inx):
        self.rnn.flatten_parameters()
        lstm_out, _ = self.rnn(inx, None)
        return lstm_out

class QA_LSTM_net():
    
    def __init__(self):
        model_path = os.path.join(dir_path,'model','zi5_vec.model')
        self.wv = KeyedVectors.load(model_path)
        self.word_dim = np.shape(self.wv[self.wv.index2word])[1]
        self.rnn = RNN(nb_hidden,self.word_dim)
        self.optimizer = torch.optim.Adam(self.rnn.parameters(), lr = learning_rate)
        #others
        self.answers = util.read_answer()
        #ready for evaluate
        self.questions = util.read_question()
        self.avg_ql = 0.0
        for q in self.questions:
            self.avg_ql += len(q)
        self.avg_ql = self.avg_ql/len(self.questions)
        file_path = os.path.join(dir_path,'model','idf_dict')
        with open(file_path, 'rb') as f:
            self.idf_dict = load(f)
        file_path = os.path.join(dir_path,'model','gram2ques')
        with open(file_path, 'rb') as f:
            self.gram2ques = load(f)
        self.restore_embed()
        self.test = 66666

    # def before_forward_match_question(self, question):
    #     """
    #     before deep learning model, match query and questions in sorpus.
    #     if find out a match one, return it.
    #     :return: False or the match question
    #     """
    #     thrshold_value = 85
    #     choices = self.questions
    #     match_question = process.extract(question, choices, limit=1)
    #     print(match_question)
    #     if match_question[0][1] >= thrshold_value:
    #         index = self.questions.index(match_question[0][0])
    #         return self.answers[index]
    #     else:
    #         return False

    def forward(self, question):
        a_embs,a_candicates = self.search_candicate(question)
        if len(a_candicates) == 0:
            return '请更具体地描述你的问题。', 0.
        q_embs = self.embed([question], max_ql)
        scores = torch.nn.functional.cosine_similarity(q_embs, a_embs)
        index = scores.data.numpy().argmax()
        score = scores.data.numpy()[index]
        return a_candicates[index],score
    
    def cal_confidence(self, question, answer):
        q_embs = self.embed([question], max_ql)
        a_embs = self.embed([answer], max_al)
        score = torch.nn.functional.cosine_similarity(q_embs, a_embs)
        return score.data.numpy()[0]
    
    def restore_embed(self):
        model_file = os.path.join(dir_path,'model','answer_embed.pkl')
        with open(model_file, 'rb') as f:
            self.answer_embedding = load(f)
    
    def embed(self, utterances, max_l):
        u_embs = np.zeros((len(utterances),max_l,self.word_dim))
        for i,u in enumerate(utterances):
            word_list = segment(u)
            word_list = [ word for word in word_list if word in self.wv ]
            word_list = word_list[:max_l]
            if not word_list:
                word_list = list('<空>')
            u_embs[i,:len(word_list)] = self.wv[word_list]
        u_embs = torch.FloatTensor(u_embs)
        u_embs = Variable(u_embs)
        u_embs = self.rnn(u_embs)
        max_pool = torch.nn.MaxPool2d(kernel_size = (max_l, 1), stride = 1)
        u_embs = max_pool(u_embs)
        u_embs = u_embs.view(-1, nb_hidden * 2)
        return u_embs
    
    def search_candicate(self, question):
        grams = extract_gram(question)
        q_candicates = set()
        for gram in grams:
            if self.idf_dict.get(gram, -1) > min_idf:
                q_candicates.update(self.gram2ques[gram])
        q_candicates = { i:self.BM25(grams, self.questions[i]) for i in q_candicates }
        sorted_q = sorted(q_candicates.items(), key = operator.itemgetter(1), reverse = True)
        a_candicates = [ self.answers[index] for (index,r) in sorted_q ]
        a_candid = [ index for (index,r) in sorted_q ]
        a_candid = a_candid[:candicate_num]
        a_candid = np.array(a_candid)
        a_embs = self.answer_embedding[a_candid.astype('int64'),:]
        a_embs = Variable(torch.Tensor(a_embs))
        return a_embs,a_candicates
    
    def BM25(self, q1_grams, q2):
        r = 0.0
        for gram in q1_grams:
            gram_count = q2.count(gram)
            r += self.idf_dict.get(gram, 0)*3*gram_count/(gram_count+0.5+1.5*len(q2)/self.avg_ql)
        return r
    
    def set_eval(self):
        self.rnn.eval()
    
    def set_train(self):
        self.rnn.train()
    
    def restore(self):
        model_file = os.path.join(dir_path,'model','main_rnn.pkl')
        self.rnn = torch.load(model_file)
        print('\n:: restoring checkpoint from', model_file, '\n')