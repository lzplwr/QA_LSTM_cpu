# -*- coding: utf-8 -*-
"""
Created on Fri May 11 15:20:41 2018

@author: hasee
"""

import torch
import os

code_path = os.path.realpath(__file__)
dir_path = os.path.dirname(code_path)

model_file = os.path.join(dir_path,'model','main_rnn.pkl')
RNN = torch.load(model_file)
RNN.cpu()

torch.save(RNN, model_file)