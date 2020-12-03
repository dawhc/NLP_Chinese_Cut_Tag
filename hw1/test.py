#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Cui Donghang
# Student ID: 1120182424


import os
import time
from .separator import Separator
from .tagger import Tagger

DIR = os.path.dirname(__file__)
TEST_FILE = os.path.join(DIR, '199806.txt')
SEP_OUTPUT_FILE = os.path.join(DIR, 'sep.out.txt')
TAG_OUTPUT_FILE = os.path.join(DIR, 'tag.out.txt')

# 统计函数运行时长装饰器
def stat_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        f = func(*args, **kwargs)
        end_time = time.time()
        print(f"[{func.__name__}] Total runtime: {1000 * (end_time - start_time)} ms.")
        return f
    return wrapper

# 分词测试函数
@stat_time
def sep_test():
    print(f"{TEST_FILE}: Seperator Testing...\n")
    s = Separator()
    fout = open(SEP_OUTPUT_FILE, 'w')
    with open(TEST_FILE, 'r') as f:
        # n: 测试集标准分词数量
        # m: 分词算法分词数量
        # c: 正确分词数量
        # count: 行数统计
        n, m, c = 0, 0, 0
        count = 0
        for line in f.readlines():
            count += 1
            std = [s.split('/')[0] for s in line.split('  ')[1:]]
            sentence = "".join(std)
            res = s.cut(sentence, dict_mode=True)
            
            fout.write(" ".join(res) + "\n")
            
            n_std = len(std)
            n_res = len(res)
            n += n_std
            m += n_res
            len_std, len_res = 0, 0
            i, j = 0, 0
            while i < n_std and j < n_res:
                if len_std < len_res:
                    len_std += len(std[i])
                    i += 1
                elif len_std > len_res:
                    len_res += len(res[j])
                    j += 1
                else:
                    if std[i] == res[j]:
                        c += 1
                    len_std += len(std[i])
                    len_res += len(res[j])
                    i += 1
                    j += 1

            print(f"\rLine {count}: total correct = {c}", end="")

        # rec: Recall 召回率
        # pre: Precision 精确率
        # f1: F1值
        rec = c / n
        pre = c / m
        f1 = 2 * rec * pre / (rec + pre)

        print(f"\nRecall = {rec}\nPrecision = {pre}\nF1 = {f1}\n")
    fout.close()

# 词性标注测试函数
@stat_time
def tag_test():
    print(f"{TEST_FILE}: Tagger Testing...\n")
    t = Tagger()
    # lines: 测试集中的行分词的列表
    # tags: 测试集中的行分词后对应的词性
    # wrods: 测试集中的所有词集合
    lines = []
    tags = []
    words = set()
    with open(TEST_FILE, 'r') as f:
        for line in f.readlines():
            line = line.strip()
            ls = [s.split('/')[0] for s in line.split('  ')[1:]]
            tag = [s.split('/')[1] for s in line.split('  ')[1:]]
            lines.append(ls)
            tags.append(tag)
            for wd in ls:
                words.add(wd)

    t.append_lib(words)
    
    # f: 词性标注结果写入文件
    f = open(TAG_OUTPUT_FILE, 'w')
    # n: 测试集中的总词数
    # c: 正确词性标注的词数
    # count: 行数统计
    n, c, count = 0, 0, 0
    for j in range(len(lines)):
        ls = lines[j]
        std = tags[j]
        count += 1
        if not ls:
            continue
        res = t.tag_with_cut_list(ls, is_add_to_lib=False)[1]
        
        n += len(ls)
        for i in range(len(ls)):
            if std[i] == res[i]:
                c += 1
        # 显示当前行数和当前正确率
        print(f"\rLine {count}: total correct = {c}, correct rate = {c/n}", end="")
        # 将该行词性标注结果写入文件
        f.write("".join([f"{ls[i]}/{res[i]}  " for i in range(len(ls))]) + '\n')
    rec = c / n
    print(f"\nTag finished! Total correct = {c}, correct rate = {c/n}\n")

    f.close()
           
  
if __name__ == '__main__':
    sep_test()
    tag_test()


