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

class Parser:
    def __init__(self, text):
        self.text = text

    def parse(self):
        tokens = []
        c = CaboCha.Parser()
        tree = c.parse(self.text)

        for i in range(tree.token_size()):
            token = tree.token(i)
            tmp = {"surface": token.surface, "normalized": token.normalized_surface, "feature": token.feature}
            tokens.append(tmp)

        for i in range(tree.chunk_size()):
            chunk = tree.chunk(i)
            print('Chunk:', i)
            print(' Link:', chunk.link)
            for j in range(chunk.token_pos, (chunk.token_pos + chunk.token_size)):
                print("   Surface: " + tokens[j]["surface"])
            print(' Head:', chunk.head_pos)  # 主辞
            print(' Func:', chunk.func_pos)  # 機能語


'''
    main
'''
if __name__ == "__main__":
    p = Parser("私の名前は中野です。")
    p.parse()
