### 程序使用说明
##### 1120182424 崔冬航
---
1. 介绍
> * 实现了对中文文本的分词以及对分词结果进行词性划分，分词可选择基于词典和基于统计两种方法，词性划分主要基于一阶HMM模型+Viterbi的方法。
> * 使用Good-Turing平滑方法对词性标注的统计数据进行平滑处理。
> * 语料库来源：《人民日报标注语料库(PFR)》
> * 词典来源：Jieba开源统计词典
2. 运行环境
> * Python 3.6 or later
3. 项目目录树
> hw1
> ├── 199801_04.simple.txt
> ├── 199801_04.txt
> ├── 199806.simple.txt
> ├── 199806.txt
> ├── convert.py
> ├── dict.txt
> ├── \_\_init\_\_.py
> ├── \_\_main\_\_.py
> ├── prob_emit.py
> ├── prob_start.py
> ├── prob_trans.py
> ├── Readme.md
> ├── separator.py
> ├── tagger.py
> └── test.py
>
> * \_\_main__.py: 模块主程序，提供命令行调用接口
> * separator.py: 分词器，实现中文分词
> * tagger.py: 词性标注器，实现中文的词性标注
> * test.py: 测试程序
> * prob_start.py: HMM分词初始状态矩阵
> * prob_emit.py: HMM分词发射矩阵
> * prob_trans.py: HMM分词状态转移矩阵
> * dict.txt: Jieba开源统计词典
> * 199801_04.txt: 《人民日报》1月到4月语料库，主要作为模型训练集
> * 199806.txt: 《人民日报》6月语料库，主要作为测试集

4. 运行方法

> * 在终端/命令行中进入项目目录的上一级目录
>
> * 使用以下命令对中文语句进行分词和i词性标注：
>
>   ```bash
>   $ python -m hw1 [sentence] [mode]
>   ```
>
>   * ``sentence``：待分词和词性标注的语句
>   * ``mode``：0/1/2，分别代表在词性标注前使用词典分词、使用统计模型分词、使用Jieba库分词。若不指定则默认为0
>
>   示例：
>
>   ```bash
>   $ python -m hw1 我们的家乡，在希望的田野上 0
>   分词中...
>   基于词典的分词结果：
>   ['我们', '的', '家乡', '，', '在', '希望', '的', '田野', '上']
>   基于统计的分词结果：
>   ['我们', '的', '家', '乡', '，', '在', '希望', '的', '田野上']
>   词性分析中...
>   词性分析结果：
>   我们/r 的/u 家乡/n ，/w 在/p 希望/v 的/u 田野/n 上/f
>   ```
>
> * 使用以下命令运行测试程序：
>
>   ```bash
>   $ python -m hw1.test
>   ```
>
>   测试程序将默认对目录下的《人民日报语料库》6月语料库（199806.txt）进行分词测试和词性标注测试。
>
>   示例：
>
>   ```bash
>   $ python -m hw1.test
>   /home/gale_force_eight/PycharmProjects/hw1/199806.txt: Seperator Testing...
>   
>   Line 24410: total correct = 1008866
>   Recall = 0.8107157264383075
>   Precision = 0.8678753156036147
>   F1 = 0.8383223183314089
>   
>   [sep_test] Total runtime: 8399.118661880493 ms.
>   /home/gale_force_eight/PycharmProjects/hw1/199806.txt: Tagger Testing...
>   
>   Line 24409: total correct = 1144968, correct rate = 0.9200853413049506
>   Tag finished! Total correct = 1144968, correct rate = 0.9200853413049506
>   
>   [tag_test] Total runtime: 2262418.1401729584 ms.
>   ```
>
> * 使用Separator进行分词：
>
>   ```python
>   from .separator import Separator
>   s = Separator()
>   result = s.cut('我们的家乡，在希望的田野上', dict_mode=True)
>   print(result)
>   ```
>
>   dict_mode：是否采用基于词典的分类方式，若为False则采用基于统计的分词方式
>
> * 使用Tagger进行词性标注：
>
>   ```python
>   from .tagger import Tagger
>   t = Tagger()
>   t.tag('我们的家乡，在希望的田野上', jieba_cut=False, dict_mode=True, is_add_to_lib=True)
>   ```
>
>   jieba_cut：是否使用jieba进行分词
>
>   dict_mode：是否采用基于词典的方式进行分词，若jieba_cut=True，则此项无效
>
>   is_add_to_lib：是否将分词结果加入到词典中，如果不加入可能造成词语无法识别错误
>
>   

5. 参数设置

> * separator.py
>
>   | 参数名    | 含义         |
>   | --------- | ------------ |
>   | DICT_PATH | 词典文件目录 |
>
> * tagger.py
>
>   | 参数名      | 含义           |
>   | ----------- | -------------- |
>   | DICT_PATH   | 词典文件目录   |
>   | CORPUS_PATH | 语料库文件目录 |
>
> * test.py
>
>   | 参数名          | 含义                 |
>   | --------------- | -------------------- |
>   | TEST_FILE       | 测试文件             |
>   | SEP_OUTPUT_FILE | 分词结果输出文件     |
>   | TAG_OUTPUT_FILE | 词性标注结果输出文件 |
>
>   

