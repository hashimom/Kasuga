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
import csv
import argparse
import numpy as np
import tensorflow as tf
from kasuga.dictool.wordvector import WordVector
from kasuga.wordholder import WordHolder


class Builder:
    def __init__(self, word_file, link_file):
        self.word_holder = WordHolder(word_file)
        self.link_list = []
        with open(link_file, encoding="utf-8") as f:
            reader = csv.reader(f, delimiter=",")
            for row in reader:
                self.link_list.append([row[0], row[1], row[2]])

        self.model = WordVector(48, 16, 8, 2)
        self.optimizer = tf.optimizers.Adam()

    def __call__(self, epoch_num, batch_size):
        for i in range(epoch_num):
            links, batch = self.make_batch(200)
            y, loss = self.train_step(batch)
            print("step " + str(i) + ": " + str(loss))

            self.update_word_id(links, y)

    @tf.function
    def train_step(self, x_data):
        with tf.GradientTape() as tape:
            y = self.model(x_data)
            loss = tf.reduce_mean(tf.square(y - x_data))
        grads = tape.gradient(loss, self.model.trainable_variables)
        self.optimizer.apply_gradients(zip(grads, self.model.trainable_variables))
        return y, loss

    def make_batch(self, batch_size):
        links = []
        batch = []
        rand_list = np.random.randint(0, len(self.link_list), batch_size)
        for i in rand_list:
            link = self.link_list[i]
            links.append(link)
            batch.append(self.word2vector(link[0]) + self.word2vector(link[1]) + self.word2vector(link[2]))
        return links, batch

    def word2vector(self, word):
        ret_ary = []
        if not word in self.word_holder.word_list:
            self.word_holder.regist(word, "未定義語", "その他")

        word_id = int(self.word_holder.word_list[word]["id"])
        for i in range(16):
            if word_id & 1:
                ret_ary.append(1.)
            else:
                ret_ary.append(0.)
            word_id = word_id >> 1
        return ret_ary

    def update_word_id(self, links, y):
        for i, link in enumerate(links):
            y_tmp = np.reshape(y[i], (3, 16))
            for j, word in enumerate(link):
                new_id = 0
                y_mean = tf.reduce_mean(y_tmp[j])
                for k in range(16):
                    if y_tmp[j][k] > y_mean:
                        new_id += 1
                    new_id = new_id << 1
                self.word_holder.word_list[word]["id"] = int(new_id)


def main():
    arg_parser = argparse.ArgumentParser()
    arg_parser.add_argument('-l', nargs='?', help='input link file', required=True)
    arg_parser.add_argument('-w', nargs='?', help='input word file', required=True)
    args = arg_parser.parse_args()

    builder = Builder(args.w, args.l)
    builder(100, 200)


if __name__ == "__main__":
    main()



