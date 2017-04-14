# coding: utf-8
from db import dbconnect
import pynlpir
import os
import json


# def load_sentence(orientation):
#     c = dbconnect.connect()
#     c.execute("select %s from pos_neg1 limit 1000" % (orientation,))
#     return [i[0] for i in c.fetchall()]


def load_sentence():
    sententce = {}
    orientation_list = ['good', 'bad']
    for orientation in orientation_list:
        sententce[orientation] = []
    dir = "../document/10000d"
    FileNames = os.listdir(dir)
    for fn in FileNames:
        f = open(dir + "/" + fn)
        js = json.loads(f.readline())
        for orientation in orientation_list:
            sententce[orientation].extend(js[orientation])
    return sententce


def get_w_a_pair():
    noun_word_map = {}
    index_noun = 0
    adj_word_map = {}
    index_adj = 0
    orientation_list = ['good', 'bad']
    noun = ['noun']
    adj = ['adjective']
    pynlpir.open()
    word_sentiment_pair = {}
    pynlpir.nlpir.ImportUserDict("userdict.txt", True)
    sententce = load_sentence()

    def find_pair(start, end):
        adj_index = index_adj
        for i in range(start, end):
            if 0 < i < len(words_list):
                word_j = words_list[i]
                if word_j[1] in adj:
                    if index_noun in word_sentiment_pair.keys():
                        if orientation in word_sentiment_pair[index_noun].keys():
                            word_sentiment_pair[index_noun][orientation].append(adj_index)
                        else:
                            word_sentiment_pair[index_noun][orientation] = [adj_index]
                    else:
                        word_sentiment_pair[index_noun] = {}
                        word_sentiment_pair[index_noun][orientation] = [adj_index]

                    if word_j[0] not in adj_word_map.keys():
                        adj_word_map[word_j[0]] = adj_index
                        adj_index += 1

                elif word_j[1] in noun:
                    break
        return adj_index

    for orientation in orientation_list:
        for sent in sententce[orientation]:
            words_list = pynlpir.segment(sent)
            for index in range(len(words_list)):
                word_i = words_list[index]
                if word_i[1] in noun:
                    index_adj = find_pair(index + 1, index + 4)
                    index_adj = find_pair(index - 3, index)
                    if word_i[0] not in noun_word_map.keys():
                        noun_word_map[word_i[0]] = index_noun
                        index_noun += 1
    return word_sentiment_pair, noun_word_map, adj_word_map


def save(ws_pair, nm, am):
    f = open("output/sentiment/word_sentiment_pair.txt")
    f.truncate()
    f.write(json.dumps(ws_pair))
    f.close()

    f = open("output/sentiment/noun_word_map.txt")
    f.truncate()
    f.write(json.dumps(nm))
    f.close()

    f = open("output/sentiment/adj_word_map.txt")
    f.truncate()
    f.write(json.dumps(am))
    f.close()
    print "save ok"


def load():
    f = open("output/sentiment/word_sentiment_pair.txt")
    ws = json.loads(f.readline())
    f.close()

    f = open("output/sentiment/noun_word_map.txt")
    nm = json.loads(f.readline())
    f.close()

    f = open("output/sentiment/adj_word_map.txt")
    am = json.loads(f.readline())
    f.close()

    return ws, nm, am


def gen_dict():
    ws, nm, am = get_w_a_pair()
    # ws, nm, am = load()
    print "ok"

gen_dict()
