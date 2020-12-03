#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Cui Donghang
# Student ID: 1120182424

from math import log
import re
import os
# emit_p: 发射矩阵
# start_p: 初始状态矩阵
# trans_p: 转移矩阵
from .prob_emit import P as emit_p
from .prob_start import P as start_p
from .prob_trans import P as trans_p
# 工作目录
DIR = os.path.dirname(__file__)
# 词典路径
DICT_PATH = os.path.join(DIR, 'dict.txt')

# Infinite value
inf = 3.14e100


class Separator(object):

    def __init__(self, dict_path=DICT_PATH):
        # 字典树，存放词典统计数据
        self.trie = {}
        self.totf = 0

        # 初始化词典和HMM模型
        self.init_dict(dict_path)
        self.init_hmm()

    # 使用词典分词的动态规划算法
    # content: 待分词语句
    def __dp(self, content):
        # 获取待分词内容的DAG
        n = len(content)
        dag = [[] for i in range(n)]
        for i in range(n):
            pw = u''
            for j in range(i, n):
                pw += content[j]
                if pw not in self.trie:
                    break
                if self.trie[pw] > 0:
                    dag[i].append(j + 1)
            if not dag[i]:
                dag[i].append(i + 1)

        # DP过程
        # f: 动态规划状态转移数组
        f = [(-inf, 0) for i in range(n + 1)]
        f[0] = (0, 0)
        for i in range(n):
            for j in dag[i]:
                val = f[i][0] + log(self.trie.get(content[i:j]) or 1) - log(self.totf)
                if f[j][0] < val:
                    f[j] = (val, i)
        sep = []
        i = n
        while i != 0:
            sep.append(i)
            i = f[i][1]

        sep.reverse()
        return sep

    # 使用HMM模型的viterbi算法
    # content: 待分词语句
    def __viterbi(self, content):
        n = len(content)
        # f: viterbi动态规划算法状态转移数组
        f = [{'B':(-inf, 'S'), 'M':(-inf, 'S'), 'E':(-inf, 'S'), 'S':(-inf, 'S')} for i in range(n)]

        for i in self.status:
            f[0][i] = (start_p[i] + emit_p[i].get(content[0], -inf), 'S')
        
        for i in range(n - 1):
            for j in self.status:
                for k in self.next_status[j]:
                    val = f[i][j][0] + trans_p[j][k] + emit_p[k].get(content[i + 1], -inf)
                    # print (f"{i}: {j}->{k}: {val}")
                    if f[i + 1][k][0] < val:
                        f[i + 1][k] = (val, j)
        cur = 'E' if f[n - 1]['E'][0] > f[n - 1]['S'][0] else 'S'
        path = cur
        
        # 寻找分词结果
        for i in range(n - 1, 0, -1):
            cur = f[i][cur][1]
            path = cur + path

        return path

    # 初始化词典
    # dict_file: 词典文件
    def init_dict(self, dict_file):
        with open(dict_file, "r") as f:
            for line in f:
                word, freq = line.strip().split(' ')[0:2]
                self.trie[word] = int(freq)
                self.totf += int(freq)
                pw = u''
                for c in word:
                    pw += c
                    if pw not in self.trie:
                        self.trie[pw] = 0

    # 初始化HMM模型
    def init_hmm(self):
        self.status = 'BMES'
        self.next_status = {
            'B': 'ME',
            'M': 'EM',
            'E': 'BS',
            'S': 'BS'
        }


    # 分词主函数
    # content: 分词内容，可以为长篇文章
    # dict_mode: 是否使用词典模式
    # 返回分词列表
    def cut(self, content, dict_mode=True):
        blocks = []

        # 正则表达式识别中文、英文大小写、字母、字符
        re_zh = re.compile("([\u4E00-\u9FD5a-zA-Z0-9+#&\._%\-]+)", re.U)
        content = re_zh.split(content)
        for sentence in content:
            if sentence == '':
                continue
            if not re_zh.match(sentence):
                blocks.append(sentence)
                continue
            if dict_mode:
                # 基于词典的分词
                result = self.__dp(sentence)
                lst = 0
                for sep in result:
                    blocks.append(sentence[lst:sep])
                    lst = sep

            else:
                # 基于统计的分词
                result = self.__viterbi(sentence)
                lst = 0
                for i in range(len(sentence)):
                    if result[i] in 'SE':
                        blocks.append(sentence[lst:i + 1])
                        lst = i + 1
                    

        return blocks

