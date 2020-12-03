#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Cui Donghang
# Student ID: 1120182424
import sys
import os
from .separator import Separator
from .tagger import Tagger

DIR = os.path.dirname(__file__)

if __name__ == '__main__':

    print('分词中...')
    s = Separator()
    if len(sys.argv) > 1:
        content = sys.argv[1]
    else:
        content = '我们的家乡，在希望的田野上'
    result = s.cut(content, dict_mode=True)
    print(f'基于词典的分词结果：\n{result}')
    result = s.cut(content, dict_mode=False)
    print(f'基于统计的分词结果：\n{result}')
    
    print('词性分析中...')
    t = Tagger() #lib_path=os.path.join(DIR, '199801.txt'))
    if len(sys.argv) > 2:
        ls, res = t.tag(content, jieba_cut=True if sys.argv[2]=='2' else False, dict_mode=True if sys.argv[2]=='0' else False)
    else:
        ls, res = t.tag(content, jieba_cut=False, dict_mode=True)
    print('词性分析结果：')
    for i in range(len(ls)):
        print("{}/{}".format(ls[i], res[i]) ,end=" ")
    print('')     
 
