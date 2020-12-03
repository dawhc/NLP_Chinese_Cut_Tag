#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Cui Donghang
# Student ID: 1120182424

'''
from math import log
import re
import os

from .prob_emit import P as emit_p
from .prob_start import P as start_p
from .prob_trans import P as trans_p
from .separator import Separator
from .tagger import Tagger

DIR = os.path.dirname(__file__)
DICT_PATH = os.path.join(DIR, 'dict.txt')
CORPUS_PATH = os.path.join(DIR, '199801.txt')

inf = 3.14e100

class Separator(object):

    def __init__(self, dict_file=DICT_PATH):
        self.trie = {}
        self.totf = 0
        self.init_dict(dict_file)
        self.init_hmm()

    def __dp(self, content):
        # Get DAG
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

        # DP
        f = [(-inf, 0) for i in range(n + 1)]
        f[0] = (0, 0)
        for i in range(n):
            for j in dag[i]:
                # print(f"{i} -> {j}: f:{f[i][0]} + w:{self.trie[content[i:j]]}, content: {content[i:j]}")
                val = f[i][0] + log(self.trie.get(content[i:j], 1)) - log(self.totf)
                if f[j][0] < val:
                    f[j] = (val, i)
        sep = []
        i = n
        while i != 0:
            sep.append(i)
            i = f[i][1]

        sep.reverse()
        return sep

    def __viterbi(self, content):
        n = len(content)
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
        for i in range(n - 1, 0, -1):
            cur = f[i][cur][1]
            path = cur + path

        return path

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

    def init_hmm(self):
        self.status = 'BMES'
        self.next_status = {
            'B': 'ME',
            'M': 'EM',
            'E': 'BS',
            'S': 'BS'
        }


    def cut(self, content, dict_mode=True):
        blocks = []

        re_zh = re.compile("([\u4E00-\u9FD5a-zA-Z0-9+#&\._%\-]+)", re.U)
        content = re_zh.split(content)
        for sentence in content:
            if not re_zh.match(sentence):
                blocks.append(sentence)
                continue
            if dict_mode:
                result = self.__dp(sentence)
                lst = 0
                for sep in result:
                    blocks.append(sentence[lst:sep])
                    lst = sep

            else:
                result = self.__viterbi(sentence)
                lst = 0
                for i in range(len(sentence)):
                    if result[i] in 'SE':
                        blocks.append(sentence[lst:i + 1])
                        lst = i + 1
                    

        return blocks[1:-1]

class Tagger(object):

    def __init__(self):

        self.tps = ['a', 'ad', 'Ag', 'b', 'c', 'd', 'Dg', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'nd', 'Ng', 'nh', 'ni', 'nl', 'nr', 'ns', 'nt', 'nz', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'Vg', 'vn','w', 'wp', 'ws', 'x', 'y', 'z']
        self.id = dict()
        self.mat = [[0 for i in range(100)] for j in range(100)]
        self.t_cnt = [0 for i in range(100)]
        self.w_cnt = dict()
        self.init_lib(CORPUS_PATH)
    
    def __stat(self, ls):
        lst = None
        for ch in ls:
            sp = ch.find('/')
            if sp == -1:
                continue
         
            wd = ch[0:sp]
            tp = self.id[ch[sp+1].lower()]
        
            self.t_cnt[tp] += 1
        
            if self.w_cnt.get(wd) is None:
                self.w_cnt[wd] = [0 for i in range(100)]
                self.w_cnt[wd][tp] += 1
            if lst is not None:
                self.mat[lst][tp] += 1
            lst = tp
    
    # Viterbi算法
    def __viterbi(self, ls):
     
        
        # print('词语/词性频度表：')
        # for w in ls:
        #     for tp in self.tps:
        #         if self.w_cnt[w][self.id[tp]] != 0:
        #             print('{}/{}: {}'.format(w, tp, self.w_cnt[w][self.id[tp]]))
            
        dp = [[0. for i in range(100)] for j in range(100)]
        dp[0] = [1. for i in range(100)]
        path = [[0 for i in range(100)] for j in range(100)]
     
        # Dp
        for i in range(len(ls) - 1):
            w = ls[i]
            w_nxt = ls[i + 1]
            for tp in self.tps:
                j = self.id[tp]
                if self.w_cnt[w][j] == 0:
                    continue
                for tp_nxt in self.tps:
                    k = self.id[tp_nxt]
                    if self.w_cnt[w_nxt][k] == 0:
                        continue
                    p = dp[i][j] * (self.mat[j][k] / self.t_cnt[j]) * (self.w_cnt[w_nxt][k] / self.t_cnt[k])
                    if p > dp[i + 1][k]:
                        dp[i + 1][k] = p
                        path[i + 1][k] = j


        # Find result
        max_p = 0
        max_tp = 0
        ans = [0 for i in range(len(ls))]
        for j in range(len(self.tps)):
            if max_p < dp[len(ls) - 1][j]:
                max_p = dp[len(ls) - 1][j]
                max_tp = j
        ans[len(ls) - 1] = max_tp
        for i in range(len(ls) - 1, 0, -1):
            max_tp = path[i][max_tp]
            ans[i - 1] = max_tp
        
        return ans
                   
    # 使用语料库初始化
    def init_lib(self, fname):
        # Initialize with a library
        for i in range(len(self.tps)):
            self.id[self.tps[i]] = i
    
    
        f = open(fname, 'r', encoding='gbk')
     
        for line in f.readlines():
            ls = line.split('  ')
            self.__stat(ls)
    # 输出语料库统计结果
    def print_stat(self):
        # Print library statistic result
        vis = [False for i in range(100)]
        print('词性频度表：')
        for tp in self.tps:
            if self.t_cnt[id[tp]] > 0:
                vis[self.id[tp]] = True
                print('{}: {}'.format(tp, self.t_cnt[self.id[tp]]))
    
        print('词性转移矩阵：')
        print('\\', end='\t')
        for tp in self.tps:
            if vis[self.id[tp]]:
                print(tp, end='\t')
    
        for tpx in self.tps:
            if not vis[self.id[tpx]]:
                continue
            print(tpx, end='\t')
            for tpy in self.tps:
                if not vis[self.id[tpy]]:
                    continue
                print(self.mat[self.id[tpx]][self.id[tpy]], end='\t')
            print('') 
     
    def tag(self, content, jieba_cut=False):
        ls = []
        if jieba_cut:
            try:
                import jieba
                ls = jieba.lcut(content)
            except ImportError:
                print('Jieba is not installed')
        else:
            s = Separator()
            ls = s.cut(content, dict_mode=True)
        result = self.__viterbi(ls)
        return (ls, [self.tps[i] for i in result])
        

            
'''
    


