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

import sys
import subprocess
import jdepp
import jaconv


class Parser:
    def __init__(self, dic_dir):
        prg_opt = ["jdepp", "-m", dic_dir]
        opt = jdepp.option(len(prg_opt), prg_opt)
        self.parser = jdepp.parser(opt)
        self.parser.init()

    def parse(self, text):
        context = {"Body": text, "Words": []}
        chunks = []

        run_cmd = "echo \"" + text + "\" | mecab"
        output = subprocess.check_output(run_cmd, shell=True)
        s = self.parser.parse_from_postagged(output)

        # 単語配列生成
        chunk = {"Independent": [], "Ancillary": [], "Link": None, "Body": text}
        for i in s.tokens():
            # 文節先頭はそれまでを保存して最初から
            if i.chunk_start and (len(chunk["Independent"]) != 0):
                chunks.append(chunk)
                chunk = {"Independent": [], "Ancillary": [], "Link": None, "Body": text}

            token = i.str().decode('utf-8')
            feature = i.feature.decode('utf-8').strip().split(',')

            # 読み取得
            if 7 < len(feature):
                read = jaconv.kata2hira(feature[7])
            else:
                # featureの要素が7個存在しない場合は恐らく記号なのでsurfaceをそのまま使う
                read = jaconv.kata2hira(token)

            tmp = {"surface": token,
                   "original": feature[6],
                   "read": read,
                   "position": [feature[0], feature[1], feature[2], feature[3]],
                   "conjugate": [feature[4], feature[5]] }

            # 自立語
            if tmp["position"][0] != u"助詞" and \
                    tmp["position"][0] != u"助動詞" and \
                    tmp["position"][1] != u"句点" and \
                    tmp["position"][1] != u"読点":
                chunk["Independent"].append(tmp)

            # 付属語先頭
            else:
                # 付属語の original は read で上書き
                tmp["original"] = tmp["read"]
                chunk["Ancillary"].append(tmp)

        # 最後の文節をここで保存
        chunks.append(chunk)

        # 係り受け情報付与
        for i, chunk in enumerate(s.chunks()):
            head = chunk.head()
            if head:
                chunks[i]["Link"] = chunks[head.id]["Independent"]

        return {"Context": context, "Chunks": chunks}

    def display(self, info):
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
    p = Parser(sys.argv[1])
    ret = p.parse("あひる焼きを食べればモリモリと元気が出るぞ")
    p.display(ret)
