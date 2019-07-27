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
import os
import json
import csv
import glob
from kasuga.reader import JsonWriter
from kasuga.wordholder import WordHolder


class PreBuilder:
    def __init__(self, in_dir, out_dir, in_text=None):
        if not os.path.isdir(out_dir):
            os.makedirs(out_dir)

        self.f_trigram = open(out_dir + "/trigram.csv", 'w')
        self.writer_trigram = csv.writer(self.f_trigram, lineterminator='\n')

        self.f_link = open(out_dir + "/link.csv", 'w')
        self.writer_link = csv.writer(self.f_link, lineterminator='\n')

        self.f_words_file = out_dir + "/words.csv"

        self.in_dir = in_dir
        self.word_holder = WordHolder()
        type_cnt = self.word_holder.type_list_cnt()
        self.soc_type = type_cnt
        self.eoc_type = [type_cnt[0], type_cnt[1]+1]

        self.jw = None
        if in_text is not None:
            self.jw = JsonWriter(in_text, in_dir)

    def __call__(self):
        print("STEP1: Text File parse...")
        if self.jw is not None:
            self.jw()

        print("STEP2: CSV file Write...")
        file_list = glob.glob(self.in_dir + "/*.json")
        for file in file_list:
            with open(file, encoding="utf-8") as in_json:
                info = json.load(in_json)

                # Word info
                for chunk in info["Chunks"]:
                    words = chunk["Independent"] + chunk["Ancillary"]
                    for word in words:
                        self.word_holder.regist(word["surface"], word["position"][0], word["position"][1])

                for chunk in info["Chunks"]:
                    # TriGram info
                    trigram_info = self.make_trigram_info(chunk)
                    for trigram in trigram_info:
                        self.writer_trigram.writerow(trigram)

                    # Link info
                    if len(chunk["Independent"]) != 0 and not chunk["Link"] is None:
                        link_info = self.make_link_info(chunk)
                        if link_info is not None:
                            self.writer_link.writerow(link_info)

        self.word_holder.save(self.f_words_file)

    def make_trigram_info(self, chunk):
        trigram = []
        words = chunk["Independent"] + chunk["Ancillary"]
        chunk_len = len(words)
        if chunk_len != 0:
            if chunk_len == 1:
                word_info = self.word_holder(words[0]["surface"])
                trigram.append(["@S@", self.soc_type[0], self.soc_type[1],
                                word_info[0], word_info[1], word_info[2],
                                "@E@", self.eoc_type[0], self.eoc_type[1]])
            else:
                for i, word in enumerate(words):
                    if i == 0:
                        tri_word = ["@S@", self.soc_type[0], self.soc_type[1]]
                    else:
                        tri_word = self.word_holder(words[i - 1]["surface"])

                    tri_word.extend(self.word_holder(word["surface"]))

                    if (i + 1) == chunk_len:
                        tri_word.extend(["@E@", self.eoc_type[0], self.eoc_type[1]])
                    else:
                        tri_word.extend(self.word_holder(words[i + 1]["surface"]))

                    trigram.append(tri_word)

        return trigram

    def make_link_info(self, chunk):
        ind_phase = ""
        lnk_phase = ""
        ind_position = [None, None]
        lnk_position = [None, None]

        # Independent
        if len(chunk["Independent"]) == 1:
            word_info = self.word_holder(chunk["Independent"][0]["surface"])
            ind_phase = word_info[0]
            ind_position = [word_info[1], word_info[2]]
        else:
            for independent in chunk["Independent"]:
                ind_phase += independent["surface"]

        # Ancillary
        if len(chunk["Ancillary"]) == 1 and chunk["Ancillary"][0]["position"][0] != "特殊":
            word_info = self.word_holder(chunk["Ancillary"][0]["surface"])
            anc_phase = word_info[0]
            anc_position = [word_info[1], word_info[2]]
        else:
            return None

        # Link
        if len(chunk["Ancillary"]) == 1:
            word_info = self.word_holder(chunk["Link"][0]["surface"])
            # lnk_phase = chunk["Link"][0]["original"]
            lnk_phase = chunk["Link"][0]["surface"]
            lnk_position = [word_info[1], word_info[2]]
        else:
            for i, link in enumerate(chunk["Link"]):
                if i == 0:
                    if link["position"][0] == "動詞" or link["position"][0] == "形容詞":
                        word_info = self.word_holder(link["surface"])
                        lnk_phase = link["original"]
                        lnk_position = [word_info[1], word_info[2]]
                        break
                lnk_phase += link["original"]

        return [ind_phase, anc_phase, lnk_phase, ind_position[0], ind_position[1],
                anc_position[0], anc_position[1], lnk_position[0], lnk_position[1]]


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-i', nargs='?', help='input json file', required=True)
    arg_parser.add_argument('-t', nargs='?', help='input text file')
    arg_parser.add_argument('-o', nargs='?', help='output CSV file', required=True)
    args = arg_parser.parse_args()

    builder = PreBuilder(args.i, args.o, args.t)
    builder()


if __name__ == "__main__":
    main()
