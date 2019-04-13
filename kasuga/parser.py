# -*- coding: utf-8 -*-
# Copyright (c) 2018-2019 Masahiko Hashimoto <hashimom@geeko.jp>
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

from pyknp import KNP


class Parser:
    def __init__(self):
        """
        Parser class
        """
        self.knp = KNP()

    def __call__(self, text):
        """
        Parser
        :param text: 入力テキスト
        :return: 解析結果(辞書型)
        """
        chunks = []
        links = []

        result = self.knp.parse(text)

        # 単語配列生成
        for bnst in result.bnst_list():
            chunk = {"Independent": [], "Ancillary": [], "Link": None}

            for mrph in bnst.mrph_list():
                tmp = {"surface": mrph.midasi,
                       "original": mrph.genkei,
                       "read": mrph.yomi,
                       "position": [mrph.hinsi, mrph.bunrui],
                       "conjugate": [mrph.katuyou1, mrph.katuyou2]
                       }

                # 自立語
                if tmp["position"][0] != "助詞" and \
                        tmp["position"][0] != "助動詞" and \
                        tmp["position"][0] != "判定詞" and \
                        tmp["position"][0] != "特殊":
                    chunk["Independent"].append(tmp)

                # 付属語先頭
                else:
                    chunk["Ancillary"].append(tmp)

            # 文節情報と係り受け情報を登録
            chunks.append(chunk)
            links.append(bnst.parent_id)

        # 係り受け情報付与
        for parent_id, link_id in enumerate(links):
            if link_id > 0:
                chunks[parent_id]["Link"] = chunks[link_id]["Independent"]

        return {"Body": text, "Chunks": chunks}

    @classmethod
    def display(cls, info):
        """
        情報表示
        :param info: 解析済み情報
        :return:
        """
        for parse in info["Chunks"]:
            print("Chunk: ")

            surface = ""
            read = ""
            original = ""
            for token in parse["Independent"]:
                surface = surface + token["surface"]
                read = read + token["read"]
                original = original + token["original"]
            print(" Independent: " + surface + "/" + read + " (" + original + ")")

            surface = ""
            read = ""
            original = ""
            for token in parse["Ancillary"]:
                surface = surface + token["surface"]
                read = read + token["read"]
                original = original + token["original"]
            print(" Ancillary: " + surface + "/" + read + " (" + original + ")")

            if parse["Link"]:
                surface = ""
                read = ""
                original = ""
                for token in parse["Link"]:
                    surface = surface + token["surface"]
                    read = read + token["read"]
                    original = original + token["original"]
                print(" Link: " + surface + "/" + read + " (" + original + ")")


if __name__ == "__main__":
    """
    main
    
    """
    p = Parser()
    ret = p("あひる焼きを食べればモリモリと、元気が出るぞよ。")
    p.display(ret)
