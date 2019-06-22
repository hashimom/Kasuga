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
import argparse
import json
from kasuga.parser import Parser


class Reader(object):
    def __init__(self, in_file, output_cb):
        self.in_file = in_file
        self.output_cb = output_cb

    def __call__(self):
        for line in open(self.in_file, 'r'):
            # 改行文字の削除
            line = line.replace('\n', '')

            # 「。」毎にパースを行う ※それ以外は未対応
            for context in line.replace("。", "。___").split("___"):
                if len(context) == 0:
                    continue

                self.parse_to_cb(context)

    def parse_to_cb(self, context):
        p = Parser()
        info = p(context)
        if info is not None:
            # パースしたデータをコールバック関数へ渡す
            self.output_cb(info)


class JsonWriter(Reader):
    def __init__(self, in_file, out_file):
        super().__init__(in_file, self.output_cb)
        self.out_file = open(out_file, 'w')

    def __call__(self):
        super().__call__()

    def output_cb(self, info):
        json.dump(info, self.out_file, indent=4, ensure_ascii=False)


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-f', nargs='?', help='input text file', required=True)
    arg_parser.add_argument('-o', nargs='?', help='output json file')
    args = arg_parser.parse_args()

    writer = JsonWriter(args.f, args.o)
    writer()


if __name__ == "__main__":
    main()
