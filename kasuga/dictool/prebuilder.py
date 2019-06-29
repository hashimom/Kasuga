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
import csv
from kasuga.reader import Reader


class PreBuilder(Reader):
    def __init__(self, in_file, out_file):
        super().__init__(in_file, self.output_cb)
        self.f = open(out_file, 'w')
        self.writer = csv.writer(self.f, lineterminator='\n')

    def __call__(self):
        super().__call__()

    def output_cb(self, info):
        for chunk in info["Chunks"]:
            if len(chunk["Independent"]) != 0 and not chunk["Link"] is None:
                ind_phase = ""
                lnk_phase = ""
                ind_position = [None, None]
                ind_conjugate = [None, None]
                lnk_position = [None, None]
                lnk_conjugate = [None, None]

                # Independent
                if len(chunk["Independent"]) == 1:
                    ind_phase = chunk["Independent"][0]["surface"]
                    ind_position = chunk["Independent"][0]["position_id"]
                    ind_conjugate = chunk["Independent"][0]["conjugate_id"]
                else:
                    for independent in chunk["Independent"]:
                        ind_phase += independent["surface"]

                # Ancillary
                if len(chunk["Ancillary"]) == 1 and chunk["Ancillary"][0]["position"][0] != "特殊":
                    anc_phase = chunk["Ancillary"][0]["surface"]
                    anc_position = chunk["Ancillary"][0]["position_id"]
                    anc_conjugate = chunk["Ancillary"][0]["conjugate_id"]
                else:
                    continue

                # Link
                if len(chunk["Ancillary"]) == 1:
                    lnk_phase = chunk["Link"][0]["surface"]
                    lnk_position = chunk["Link"][0]["position_id"]
                    lnk_conjugate = chunk["Link"][0]["conjugate_id"]
                else:
                    for i, link in enumerate(chunk["Link"]):
                        if i == 0:
                            if link["position"][0] == "動詞" or link["position"][0] == "形容詞":
                                lnk_phase = link["surface"]
                                lnk_position = link["position_id"]
                                lnk_conjugate = link["conjugate_id"]
                                break
                        lnk_phase += link["surface"]

                self.writer.writerow([ind_phase, anc_phase, lnk_phase,
                                      ind_position[0], ind_position[1], ind_conjugate[0], ind_conjugate[1],
                                      anc_position[0], anc_position[1], anc_conjugate[0], anc_conjugate[1],
                                      lnk_position[0], lnk_position[1], lnk_conjugate[0], lnk_conjugate[1]])


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-i', nargs='?', help='input text file', required=True)
    arg_parser.add_argument('-o', nargs='?', help='output CSV file', required=True)
    args = arg_parser.parse_args()

    builder = PreBuilder(args.i, args.o)
    builder()


if __name__ == "__main__":
    main()
