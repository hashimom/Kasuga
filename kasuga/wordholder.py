# -*- coding: utf-8 -*-
"""
 Copyright (c) 2018-2019 Masahiko Hashimoto <hashimom@geeko.jp>

 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:

 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.

 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 SOFTWARE.
"""
import csv
import numpy as np

WORD_TYPE_LIST = [
    [
        "形容詞",
        "連体詞",
        "副詞",
        "判定詞",
        "助動詞",
        "接続詞",
        "指示詞",
        "感動詞",
        "名詞",
        "動詞",
        "助詞",
        "接頭辞",
        "接尾辞",
        "特殊",
        "未定義語"
    ],
    [
        "形容詞",
        "連体詞",
        "副詞",
        "判定詞",
        "助動詞",
        "接続詞",
        "名詞形態指示詞",
        "連体詞形態指示詞",
        "副詞形態指示詞",
        "感動詞",
        "普通名詞",
        "副詞的名詞",
        "形式名詞",
        "固有名詞",
        "組織名",
        "地名",
        "人名",
        "サ変名詞",
        "数詞",
        "時相名詞",
        "動詞",
        "格助詞",
        "副助詞",
        "接続助詞",
        "終助詞",
        "名詞接頭辞",
        "動詞接頭辞",
        "イ形容詞接頭辞",
        "ナ形容詞接頭辞",
        "名詞性名詞接尾辞",
        "名詞性述語接尾辞",
        "名詞性名詞助数辞",
        "名詞性特殊接尾辞",
        "形容詞性述語接尾辞",
        "形容詞性名詞接尾辞",
        "動詞性接尾辞",
        "句点",
        "読点",
        "括弧始",
        "括弧終",
        "記号",
        "空白",
        "カタカナ",
        "アルファベット",
        "その他"
    ]
]


class WordHolder:
    def __init__(self, list_file=None):
        self.word_list = {}

        # word file read
        if list_file is not None:
            with open(list_file, "r", encoding="utf-8") as f:
                reader = csv.reader(f, delimiter=",")
                for row in reader:
                    self.word_list[row[0]] = {"id": row[1], "type1": row[2], "type2": row[3]}

    def __call__(self, surface):
        return [surface, self.word_list[surface]["type1"], self.word_list[surface]["type2"]]

    def regist(self, surface, type1, type2):
        if not surface in self.word_list:
            word_id = np.random.randint(0, 65535)
            if type2 != "*":
                self.word_list[surface] = {"id": word_id,
                                           "type1": WORD_TYPE_LIST[0].index(type1),
                                           "type2": WORD_TYPE_LIST[1].index(type2)}
            else:
                self.word_list[surface] = {"id": word_id,
                                           "type1": WORD_TYPE_LIST[0].index(type1),
                                           "type2": WORD_TYPE_LIST[0].index(type1)}

    def save(self, filename):
        with open(filename, 'w') as f:
            writer = csv.writer(f, lineterminator='\n')
            for k, v in self.word_list.items():
                writer.writerow([k, v["id"], v["type1"], v["type2"]])

    @staticmethod
    def get_rand_id(word_id):
        ret_ary = []
        tmp = word_id
        for i in range(16):
            if tmp & 1:
                ret_ary.append(1)
            else:
                ret_ary.append(0)
            tmp = tmp >> 1
        return ret_ary

    @staticmethod
    def type_list_cnt():
        return [len(WORD_TYPE_LIST[0]), len(WORD_TYPE_LIST[1])]


