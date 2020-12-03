#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Cui Donghang
# Student ID: 1120182424
# 
# 简化训练集和测试集：去除“[]”及其标注的词性
import os
import re

# 工作目录
DIR = os.path.dirname(__file__)
INPUT_FILE = os.path.join(DIR, '199806.txt')
OUTPUT_FILE = os.path.join(DIR, '199806.simple.txt')

def convert(s):
    p = re.compile('\[(.+?)\][a-z]{0,2}')
    while True:
        res = re.search(p, s)
        if res is None:
            break
        l, r = res.span()
        s = s[:l] + res.group(1) + s[r:]
    return s

if __name__ == '__main__':
    fin = open(INPUT_FILE, 'r', encoding='utf-8')
    fout = open(OUTPUT_FILE, 'w', encoding='utf-8')

    count = 0
    for line in fin.readlines():
        count += 1
        print(f"\rConverting...line {count}", end="")
        fout.write(convert(line))

