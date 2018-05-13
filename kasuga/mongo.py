# -*- coding: utf-8 -*-
# Copyright (c) 2018 Masahiko Hashimoto <hashimom@geeko.jp>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from pymongo import MongoClient

mongodbHostName = 'localhost'
mongodbPortNo = 27017

class Mongo:
    def __init__(self, name):
        self.name = name
        client = MongoClient(mongodbHostName, mongodbPortNo)
        db = client.kasuga
        self.contexts = db.contexts
        self.phases = db.phases
        self.words = db.words

    def regist(self, info):
        if self.contexts.find({"Name": self.name, "Body": info["Context"]["Body"]}).count() == 0:
            # 形態素解析情報登録
            self.contexts.insert({"Name": self.name, "Body": info["Context"]["Body"], "Words": info["Context"]["Words"]})

            # 単語情報登録
            for w in info["Context"]["Words"]:
                if self.words.find(w).count() == 0:
                    self.words.insert(w)

            # 文節情報登録
            for p in info["Phases"]:
                self.phases.insert(p)
