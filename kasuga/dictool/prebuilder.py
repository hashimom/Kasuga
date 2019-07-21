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


class PreBuilder:
    def __init__(self, in_dir, out_dir, in_text=None):
        if not os.path.isdir(out_dir):
            os.makedirs(out_dir)

        self.f_trigram = open(out_dir + "/trigram.csv", 'w')
        self.writer_trigram = csv.writer(self.f_trigram, lineterminator='\n')

        self.f_link = open(out_dir + "/link.csv", 'w')
        self.writer_link = csv.writer(self.f_link, lineterminator='\n')

        self.in_dir = in_dir
        self.jw = None
        if in_text is not None:
            self.jw = JsonWriter(in_text, in_dir)

    def __call__(self):
        print("STEP1: Text File parse...")
        if self.jw is not None:
            self.jw()

        print("STEP2: CSV File Write...")
        file_list = glob.glob(self.in_dir + "/*.json")
        for file in file_list:
            with open(file, encoding="utf-8") as in_json:
                info = json.load(in_json)
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

    @staticmethod
    def make_trigram_info(chunk):
        trigram = []
        words = chunk["Independent"] + chunk["Ancillary"]
        chunk_len = len(words)
        if chunk_len != 0:
            if chunk_len == 1:
                trigram.append(["@SOC@", 0, 0,
                                words[0]["surface"], words[0]["position_id"][0], words[0]["position_id"][1],
                                "@EOC@", 0, 0])
            else:
                for i, word in enumerate(words):
                    if i == 0:
                        tri_word = ["@SOC@", 0, 0]
                    else:
                        tri_word = [words[i - 1]["surface"],
                                    words[i - 1]["position_id"][0],
                                    words[i - 1]["position_id"][1]]

                    tri_word.extend([word["surface"], word["position_id"][0], word["position_id"][1]])

                    if (i + 1) == chunk_len:
                        tri_word.extend(["@EOC@", 0, 0])
                    else:
                        tri_word.extend([words[i + 1]["surface"],
                                         words[i + 1]["position_id"][0],
                                         words[i + 1]["position_id"][1]])

                    trigram.append(tri_word)

        return trigram

    @staticmethod
    def make_link_info(chunk):
        ind_phase = ""
        lnk_phase = ""
        ind_position = [None, None]
        lnk_position = [None, None]

        # Independent
        if len(chunk["Independent"]) == 1:
            ind_phase = chunk["Independent"][0]["surface"]
            ind_position = chunk["Independent"][0]["position_id"]
        else:
            for independent in chunk["Independent"]:
                ind_phase += independent["surface"]

        # Ancillary
        if len(chunk["Ancillary"]) == 1 and chunk["Ancillary"][0]["position"][0] != "特殊":
            anc_phase = chunk["Ancillary"][0]["surface"]
            anc_position = chunk["Ancillary"][0]["position_id"]
        else:
            return None

        # Link
        if len(chunk["Ancillary"]) == 1:
            lnk_phase = chunk["Link"][0]["original"]
            lnk_position = chunk["Link"][0]["position_id"]
        else:
            for i, link in enumerate(chunk["Link"]):
                if i == 0:
                    if link["position"][0] == "動詞" or link["position"][0] == "形容詞":
                        lnk_phase = link["original"]
                        lnk_position = link["position_id"]
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
