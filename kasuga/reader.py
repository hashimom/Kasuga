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

import argparse
import json
from kasuga.parser import Parser


class Reader:
    def __init__(self, in_file, out_file=None):
        self.in_file = in_file
        self.out_file = out_file

    def __call__(self):
        infos = []

        for line in open(self.in_file, 'r'):
            # 改行文字の削除
            line = line.replace('\n', '')

            # 「。」毎にパースを行う ※それ以外は未対応
            for context in line.replace("。", "。___").split("___"):
                if len(context) == 0:
                    continue

                p = Parser()
                info = p(context)
                if self.out_file is not None:
                    with open(self.out_file, 'w') as f:
                        json.dump(info, f, indent=4, ensure_ascii=False)

                infos.append(info)

        return infos


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-f', nargs='?', help='input text file', required=True)
    arg_parser.add_argument('-o', nargs='?', help='output json file')
    args = arg_parser.parse_args()

    reader = Reader(args.f, args.o)
    reader()


if __name__ == "__main__":
    main()
