#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Cui Donghang
# Student ID: 1120182424

import os 
from math import log
from .separator import Separator

# DIR: 工作目录
# DICT_PATH: 词典文件路径
# CORPUS_PATH: 《人民日报》语料库路径
DIR = os.path.dirname(__file__)
DICT_PATH = os.path.join(DIR, 'dict.txt')
CORPUS_PATH = os.path.join(DIR, '199801_04.txt')

# Infinite value
inf = 3.14e100

class Tagger(object):

    def __init__(self, dict_path=DICT_PATH, lib_path=CORPUS_PATH):
        # tps: 词性集合
        self.tps = ['a', 'ad', 'Ag', 'b', 'c', 'd', 'Dg', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'nd', 'Ng', 'nh', 'ni', 'nl', 'nr', 'ns', 'nt', 'nz', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'Vg', 'vn','w', 'wp', 'ws', 'x', 'y', 'z', 'an', 'vd', 'Tg', 'nx', 'Bg', 'Rg', 'Mg', 'Yg']
        self.tsz = len(self.tps)
        self.tid = dict()
        self.wid = dict()
        self.wtot = 0
        # mat: 词性转移矩阵
        self.mat = [[0 for i in range(self.tsz)] for j in range(self.tsz)]
        # t_cnt: 初始状态矩阵
        self.t_cnt = [0 for i in range(self.tsz)]
        # w_cnt: 发射矩阵
        self.w_cnt = [[] for i in range(self.tsz)]
        # w_prob: 平滑后的发射矩阵
        self.w_prob = [[] for i in range(self.tsz)]
        for i in range(self.tsz):
            self.tid[self.tps[i]] = i

        # 初始化词典和语料库
        self.init_lib(dict_path, lib_path)
        
            
    # Good-Turing平滑算法
    # counts: 待平滑的列表
    @staticmethod
    def good_turing(counts):
        N = sum(counts)
        # 存储平滑后的值
        prob = [0] * len(counts)
    
        if N == 0:
            return prob
        
        Nr = [0] * (max(counts) + 1)
        for r in counts:
            Nr[r] += 1
        # 平滑范围，只对r小于8的值进行平滑
        smooth_boundary = min(len(Nr)-1, 8)  

        # 平滑过程
        for r in range(smooth_boundary):
            if Nr[r] != 0 and Nr[r+1] != 0:
                Nr[r] = (r+1) * Nr[r+1] / Nr[r]
            else:
                Nr[r] = r
        for r in range(smooth_boundary, len(Nr)):
            Nr[r] = r
       
        for i in range(len(counts)):
            prob[i] = Nr[counts[i]]
        total = sum(prob)

        # 归一化
        return [p/total for p in prob]
    
    # Viterbi算法
    # ls: 分词后的词列表
    def __viterbi(self, ls):
        if not ls:
            return []

        n = len(ls)

        # dp: 动态规划的状态转移数组
        dp = [[-inf for i in range(self.tsz)] for j in range(n + 10)]
        # path: 动态规划的状态转移路径数组
        path = [[0 for i in range(self.tsz)] for j in range(n + 10)]
        # 初始化dp数组 
        for tp in self.tps:
            i = self.tid[tp]
            dp[0][i] = (log(self.t_cnt[i]) if self.t_cnt[i] != 0 else -inf) + \
                (log(self.w_prob[i][self.wid[ls[0]]]) if self.w_prob[i][self.wid[ls[0]]] != 0 else -inf)
        

        # Viterbi
        for i in range(n - 1):
            w = ls[i]
            w_nxt = ls[i + 1]
            for tp in self.tps:
                j = self.tid[tp]
                wj = self.wid[w]
                for tp_nxt in self.tps:
                    k = self.tid[tp_nxt]
                    wk = self.wid[w_nxt]
                    p = dp[i][j] + \
                        (log(self.mat[j][k]) if self.mat[j][k] != 0 else -inf) + \
                        (log(self.w_prob[k][wk]) if self.w_prob[k][wk] != 0 else -inf)
                    if p > dp[i + 1][k]:
                        dp[i + 1][k] = p
                        path[i + 1][k] = j


        # 寻找状态转移路径
        max_p = -inf
        max_tp = 0
        ans = [0 for i in range(n + 1)]
        for j in range(self.tsz):
            if max_p < dp[n - 1][j]:
                max_p = dp[n - 1][j]
                max_tp = j
        ans[n - 1] = max_tp
        for i in range(n - 1, 0, -1):
            max_tp = path[i][max_tp]
            ans[i - 1] = max_tp
        return ans
                   
    # 使用语料库初始化
    # dict_file: 词典文件路径
    # corpus_file: 语料库文件路径
    def init_lib(self, dict_file, corpus_file):
        # 初始化词典 
        with open(dict_file, 'r') as f:
            for line in f.readlines():
                wd = line.split(' ')[0]
                self.wtot += 1
                self.wid[wd] = self.wtot;

        
        for i in self.tid.values():
            self.w_cnt[i] = [0 for j in range(self.wtot + 1)]

        # 初始化语料库
        with open(corpus_file, 'r', encoding='utf-8') as f:
            for line in f.readlines():
                ls = line.strip().split('  ')
                lst = None
                for ch in ls:
                    try:
                        wd, tp = ch.split('/')[0:2]
                    except ValueError:
                        continue
                    if self.wid.get(wd) is None:
                        self.wtot += 1
                        self.wid[wd] = self.wtot
                        for i in self.tid.values():
                            self.w_cnt[i].append(0)
                    wd = self.wid[wd]
                    tp = self.tid[tp.split(']')[0]]
                    
                    self.t_cnt[tp] += 1
                    self.w_cnt[tp][wd] += 1
                    if lst is not None:
                        self.mat[lst][tp] += 1
                    lst = tp

        # 平滑统计结果
        for t in range(self.tsz):
            self.w_prob[t] = self.good_turing(self.w_cnt[t])
            self.mat[t] = self.good_turing(self.mat[t])
        self.t_cnt = self.good_turing(self.t_cnt)

    # 加入新词汇    
    # ls: 词汇列表
    def append_lib(self, ls):
        for w in ls:
            if self.wid.get(w) is None:
                self.wtot += 1
                self.wid[w] = self.wtot
                for t in range(self.tsz):
                    self.w_cnt[t].append(0)
         
        for t in range(self.tsz):
            self.w_prob[t] = self.good_turing(self.w_cnt[t])
         
    # 对已经分词的列表进行词性标注
    # ls: 分词列表
    def tag_with_cut_list(self, ls, is_add_to_lib=True):
        if is_add_to_lib:
            self.append_lib(ls)
        result = self.__viterbi(ls)
        return (ls, [self.tps[i] for i in result])
    
    # 对句子进行分词和词性标注
    # content: 待分词内容
    # jieba_cut: 是否使用jieba进行分词
    # dict_mode: 是否使用Separator的词典模式进行分词
    # 返回二元组: (分词结果列表, 词性标注列表)
    def tag(self, content, jieba_cut=False, dict_mode=True, is_add_to_lib=True):
        ls = []
        if jieba_cut:
            try:
                import jieba
                ls = jieba.lcut(content)
            except ImportError:
                print('Jieba is not installed')
        else:
            s = Separator()
            ls = s.cut(content, dict_mode=dict_mode)
        return self.tag_with_cut_list(ls, is_add_to_lib)


