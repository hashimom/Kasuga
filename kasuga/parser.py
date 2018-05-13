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

import CaboCha
import jaconv

class Parser:
    def __init__(self, text):
        self.text = text
        self.context = {"Body": text, "Words": []}
        self.phases = []

    def parse(self):
        c = CaboCha.Parser()
        tree = c.parse(self.context["Body"])

        # 単語配列生成
        tokens = []
        for i in range(tree.token_size()):
            token = tree.token(i)
            feature = token.feature.strip().split(',')

            # 読み取得
            if 7 < len(feature):
                read = jaconv.kata2hira(feature[7])
            else:
                # featureの要素が7個存在しない場合は恐らく記号なのでsurfaceをそのまま使う
                read = jaconv.kata2hira(token.surface)

            tmp = {"surface": token.surface,
                   "original": feature[6],
                   "read": read,
                   "position": [feature[0], feature[1], feature[2], feature[3]],
                   "conjugate": [feature[4], feature[5]] }
            tokens.append(tmp)

        # 文節情報生成
        for i in range(tree.chunk_size()):
            chunk = tree.chunk(i)
            phase = {"Independent": {}, "Ancillary": None, "Link": None}
            for j in range(chunk.token_pos, (chunk.token_pos + chunk.token_size)):
                # 1: 自立語先頭
                if len(phase["Independent"]) == 0:
                    phase["Independent"] = tokens[j]

                # 2: 自立語、且つ先頭以外
                elif phase["Ancillary"] is None and \
                    tokens[j]["position"][0] != "助詞" and \
                    tokens[j]["position"][0] != "助動詞" and \
                    tokens[j]["position"][1] != "句点" and \
                    tokens[j]["position"][1] != "読点":
                    # surface, original, read を結合する
                    phase["Independent"]["surface"] = phase["Independent"]["surface"] + tokens[j]["surface"]
                    phase["Independent"]["original"] = phase["Independent"]["original"] + tokens[j]["original"]
                    phase["Independent"]["read"] = phase["Independent"]["read"] + tokens[j]["read"]

                # 3: 付属語先頭
                elif phase["Ancillary"] is None:
                    phase["Ancillary"] = tokens[j]
                    # 付属語の original は read で上書き
                    phase["Ancillary"]["original"] = tokens[j]["read"]

                # 4: 付属語、且つ先頭以外
                else:
                    # surface, original, read を結合する
                    phase["Ancillary"]["surface"] = phase["Ancillary"]["surface"] + tokens[j]["surface"]
                    phase["Ancillary"]["original"] = phase["Ancillary"]["original"] + tokens[j]["read"]
                    phase["Ancillary"]["read"] = phase["Ancillary"]["read"] + tokens[j]["read"]

            # 単語情報登録
            self.context["Words"].append(phase["Independent"])
            self.context["Words"].append(phase["Ancillary"])

            # 文節情報登録
            phase["Body"] = self.text
            self.phases.append(phase)

        # 係り受け情報付与
        for i in range(tree.chunk_size()):
            link = tree.chunk(i).link
            if link != -1:
                self.phases[i]["Link"] = self.phases[link]["Independent"]


        return({"Context":self.context, "Phases":self.phases})

    def display(self):
        for parse in self.phases:
            print("Chunk: ")
            print(" Independent: " + parse["Independent"]["surface"] + "/" +
                  parse["Independent"]["read"] + " (" +
                  parse["Independent"]["original"] + ")")
            if parse["Ancillary"]:
                print(" Ancillary:   " + parse["Ancillary"]["surface"] + "/" +
                      parse["Ancillary"]["read"] + " (" +
                      parse["Ancillary"]["original"] + ")")
            if parse["Link"]:
                print(" Link:   " + parse["Link"]["surface"] + "/" +
                      parse["Link"]["read"] + " (" +
                      parse["Link"]["original"] + ")")


'''
    main
'''
if __name__ == "__main__":
    p = Parser("あひる焼きを食べればモリモリと元気が出るぞ")
    ret = p.parse()
    p.display()
