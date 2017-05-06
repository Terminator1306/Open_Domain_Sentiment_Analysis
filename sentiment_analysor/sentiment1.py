# coding: utf-8
import codecs
import json
import sys
import time
import urllib2

from copy import deepcopy

from db import dbconnect
import Levenshtein
import collections

import HowNet
from sentiment_analysor import aspect_tree

reload(sys)
sys.setdefaultencoding('utf-8')



def load_data():
    negative_words = []
    positive_words = []
    deny_words = []
    degree1 = []
    degree2 = []
    degree3 = []
    degree4 = []
    degree5 = []
    degree6 = []
    feature = []

    for i in open(u"sentiment_analysor/sentiment_data/negative_words.txt", "r"):
        s = i.strip()
        negative_words.append(s.decode('gbk'))
    for i in open(u"sentiment_analysor/sentiment_data/positive_words.txt", "r"):
        s = i.strip()
        positive_words.append(s.decode('gbk'))
    for i in open(u"sentiment_analysor/sentiment_data/deny_words.txt", "r"):
        s = i.strip()
        if s[:3] == codecs.BOM_UTF8:
            s = s[3:]
        deny_words.append(s.decode('utf-8'))
    for i in open(u"sentiment_analysor/sentiment_data/d1.txt", 'r'):
        s = i.strip()
        if s[:3] == codecs.BOM_UTF8:
            s = s[3:]
        degree1.append(s.decode('utf-8'))
    for i in open(u"sentiment_analysor/sentiment_data/d2.txt", 'r'):
        s = i.strip()
        if s[:3] == codecs.BOM_UTF8:
            s = s[3:]
        degree2.append(s.decode('utf-8'))
    for i in open(u"sentiment_analysor/sentiment_data/d3.txt", 'r'):
        s = i.strip()
        if s[:3] == codecs.BOM_UTF8:
            s = s[3:]
        degree3.append(s.decode('utf-8'))
    for i in open(u"sentiment_analysor/sentiment_data/d4.txt", 'r'):
        s = i.strip()
        if s[:3] == codecs.BOM_UTF8:
            s = s[3:]
        degree4.append(s.decode('utf-8'))
    for i in open(u"sentiment_analysor/sentiment_data/d5.txt", 'r'):
        s = i.strip()
        if s[:3] == codecs.BOM_UTF8:
            s = s[3:]
        degree5.append(s.decode('utf-8'))
    for i in open(u"sentiment_analysor/sentiment_data/d6.txt", 'r'):
        s = i.strip()
        if s[:3] == codecs.BOM_UTF8:
            s = s[3:]
        degree6.append(s.decode('utf-8'))
    for i in open('sentiment_analysor/aspect_data/phone/aspect.txt', 'r'):
        feature.append(i.strip().decode('utf-8').split(','))

    return feature, negative_words, positive_words, deny_words, [degree1, degree2, degree3, degree4, degree5, degree6]


def get_dp(text, count=0):
    url_get_base = "http://api.ltp-cloud.com/analysis/?"
    api_key = 'u7U8a049FR0h1QGs4h9aTKDi6M3WpYnqGm2oagQg'
    form = 'json'
    patt = 'dp'
    try:
        result = urllib2.urlopen(
            "%sapi_key=%s&text=%s&format=%s&pattern=%s" % (url_get_base, api_key, text, form, patt))
        content = json.loads(result.read().strip())
        time.sleep(2)
    except Exception, e:
        print "try again"
        time.sleep(10)
        if count < 5:
            return get_dp(text, count + 1)
        else:
            return []
    return content

def compute_coefficient(pair):
    if len(pair[2]) == 1:
        if len(pair[3]) > 0:
            max_degree = 0
            min_degree_index = 10000

            # 程度副词的的位置
            for d in pair[3]:
                if d['index'] < min_degree_index:
                    min_degree_index = d['index']
                if d['degree'] > max_degree:
                    max_degree = d['degree']

            # 否定词的位置
            deny_index = pair[2][0]['index']
            if deny_index < min_degree_index:
                coeff = -0.4 * max_degree
            else:
                coeff = -1 * max_degree
        else:
            coeff = -1

    elif len(pair[2]) > 1:
        if len(pair[2]) % 2 == 1:
            p_n = -1
        else:
            p_n = 1

        if len(pair[3]) > 0:
            max_degree = 0
            for d in pair[3]:
                if d['degree'] > max_degree:
                    max_degree = d['degree']
            coeff = p_n * max_degree
        else:
            coeff = p_n

    else:
        if len(pair[3]) > 0:
            coeff = 0
            for d in pair[3]:
                if d['degree'] > coeff:
                    coeff = d['degree']
        else:
            coeff = 1

    return coeff


def compute_sentiment(text):
    # 直接宾语中挖掘极性动词，
    feature, negative_words, positive_words, deny_words, degrees = load_data()
    pair_set = []
    dp = []

    def get_feature(index):
        feature_temp = [dp[index]['cont']]
        i = index - 1
        while i >= 0:
            if dp[i]['relate'] == 'ATT' and dp[i]['parent'] == index:
                feature_temp.append(dp[i]['cont'])
                index = i
            i -= 1

        result = []
        for f in feature:
            if set(f).issubset(feature_temp):
                result.append(tuple(f))

        # return feature_temp
        return result

    def sentiment_value(word):
        if word in positive_words:
            return 1
        if word in negative_words:
            return -1

        for w in positive_words:
            sim = HowNet.similar_word(w, word)
            if sim > 0.8 or sim is None and Levenshtein.jaro(w, word) > 0.9:
                positive_words.append(w)
                return 1

        for w in negative_words:
            sim = HowNet.similar_word(w, word)
            if sim > 0.8 or sim is None and Levenshtein.jaro(w, word) > 0.9:
                negative_words.append(w)
                return -1

        return 0

    def is_deny_word(word):
        if word in deny_words:
            return True
        for w in deny_words:
            sim = HowNet.similar_word(w, word)
            if sim > 0.8:
                deny_words.append(w)
                return True

    def degree(word):
        # word = word.encode("utf-8")
        de = -1
        for a, d in enumerate(degrees):
            if word in d:
                de = a
                break
            for w in d:
                sim = HowNet.similar_word(w, word)
                if sim > 0.8 and sim is None and Levenshtein.jaro(w, word) > 0.8:
                    d.append(w)
                    de = a
                    break
        if de in [0, 5]:
            value = 1.6
        elif de == 1:
            value = 1.4
        elif de == 2:
            value = 1.2
        elif de == 3:
            value = 0.8
        elif de == 4:
            value = 0.6
        else:
            return -1
        return value

    def get_deny_degree(index):
        # 提取index前的程度副词及否定词
        deny_word = []
        deg = []
        for i in range(0, index)[::-1]:
            if dp[i]['relate'] in ['SBV', 'COO', 'VOB', 'WP']:
                break

            if dp[i]['relate'] in ['ADV', 'HED']:
                if is_deny_word(dp[i]['cont']):
                    dp[i]['index'] = i
                    deny_word.append(dp[i])
                else:
                    de = degree(dp[i]['cont'])
                    if de > 0:
                        dp[i]['index'] = i
                        dp[i]['degree'] = de
                        deg.append(dp[i])

        return deny_word, deg

    def yield_pair(val, ind, feature_list):
        if len(feature_list) > 0:
            deny_word, deg = get_deny_degree(ind)
            if val == 0:
                # 寻找情感词
                for index in range(max(0, ind - 3), ind)[::-1]:
                    if val != 0:
                        break
                    if dp[index]['relate'] == 'WP':
                        break
                    elif dp[index]['relate'] in ['ADV', 'HED', 'CMP']:
                        val += sentiment_value(dp[index]['cont'])
                for index in range(ind + 1, min(len(dp), ind + 6)):
                    if val != 0:
                        break
                    if dp[index]['relate'] == 'WP':
                        break
                    elif dp[index]['relate'] in ['ADV', 'HED', 'CMP']:
                        val += sentiment_value(dp[index]['cont'])

                # 寻找否定词及程度副词
                if val != 0:
                    for index in range(max(0, ind - 3), ind)[::-1]:
                        if dp[index]['relate'] == 'WP':
                            break
                        elif dp[index]['relate'] in ['ADV', 'HED']:
                            de = degree(dp[index]['cont'])
                            if de > 0:
                                dp[index]['index'] = index
                                dp[index]['degree'] = de
                                deg.append(dp[index])
                            if is_deny_word(dp[index]['cont']):
                                dp[index]['index'] = index
                                deny_word.append(dp[index])

                    for index in range(ind+1, min(len(dp), ind + 6)):
                        if dp[index]['relate'] == 'WP':
                            break
                        elif dp[index]['relate'] in ['ADV', 'HED']:
                            de = degree(dp[index]['cont'])
                            if de > 0:
                                dp[index]['index'] = index
                                dp[index]['degree'] = de
                                deg.append(dp[index])
                            if is_deny_word(dp[index]['cont']):
                                dp[index]['index'] = index
                                deny_word.append(dp[index])
            if val != 0:
                pair_set.append([feature_list, val, deny_word, deg])

    def find_sbv_coo(ind, feature_list):
        i = ind + 1
        while i < len(dp):
            if dp[i]['relate'] == 'COO' and dp[i]['parent'] == ind:
                follow = False
                for j in range(i + 1, len(dp)):
                    if dp[j]['parent'] == i and dp[j]['relate'] != 'COO':
                        follow = True
                if not follow:
                    value = sentiment_value(dp[i]['cont'])
                    yield_pair(value, i, feature_list)
            if dp[i]['relate'] in ["SBV", "VOB"]:
                break
            i += 1

    def find_vob_coo_feature(ind, feature_list):
        for i in range(ind+1, len(dp)):
            if dp[i]['relate'] == 'COO' and dp[i]['parent'] == ind:
                feature_list.extend(get_feature(i))

    # def adv_value(a, b):
    #     ad_value = 1
    #     for word_index in range(a, b):
    #         if dp[word_index]['relate'] == 'ADV':
    #             v = sentiment_value(dp[word_index]['cont'])
    #             if v!= 0:
    #                 ad_value *= v
    #     return ad_value

    def get_pair():
        for index, relation in enumerate(dp):
            if relation['relate'] == 'SBV':  # 主谓结构
                feature_list = get_feature(index)

                for i in range(index + 1, relation['parent'] + 1):
                    if dp[i]['relate'] == 'POB':  # 主谓结构中有介宾关系 如：我对手机很满意
                        feature_list.extend(get_feature(i))

                if len(feature_list) > 0:  # 主谓结构谓语通常是情感词
                    follow = False
                    for j in range(relation['parent']+1, len(dp)):
                        if dp[j]['parent'] == relation['parent'] and dp[j]['relate'] == 'VOB':
                            follow = True
                            break
                    if not follow:
                        value = sentiment_value(dp[relation['parent']]['cont'])
                        # value *= adv_value(index + 1, relation['parent']) # 应该记录
                        yield_pair(value, relation['parent'], feature_list)
                    find_sbv_coo(relation['parent'], feature_list)

            elif relation['relate'] == 'VOB':  # 动宾关系
                feature_list = get_feature(index)
                # 宾语是特征词，谓语表达情感倾向，例如 很喜欢手机外观
                if len(feature_list) > 0:
                    find_vob_coo_feature(index, feature_list)
                    value = sentiment_value(dp[relation['parent']]['cont'])
                    yield_pair(value, relation['parent'], feature_list)

                # 宾语是情感词,找到特征词主语 例如，手机用着很流畅
                else:
                    value = sentiment_value(relation['cont'])
                    if value != 0:
                        i = relation['parent']
                        pred = [relation['parent']]  # 所有并列关系的谓语下标

                        while i >= 0:
                            if dp[i]['relate'] in ['VOB']:
                                break
                            if dp[i]['relate'] == 'SBV':
                                if dp[i]['parent'] in pred:
                                    feature_list.extend(get_feature(i))
                                break
                            if dp[i]['relate'] == 'POB':  # 找到这个谓语临近的介宾短语，提取特征词
                                feature_list.extend(get_feature(i))
                            if dp[i]['relate'] == 'COO':
                                flag = False
                                for m in range(dp[i]['parent'],i):
                                    if dp[m]['relate'] in ['SBV', 'VOB']:
                                        if dp[m]['parent'] in pred:
                                            feature_list.extend(get_feature(i))
                                        flag = True
                                        break
                                if not flag:
                                    i = dp[i]['parent']
                                    pred.append(i)
                                    continue
                            i -= 1
                        yield_pair(value, index, feature_list)

    a = get_dp(text)
    for i in a:
        for j in i:
            dp = j
            get_pair()

    result = {}
    # for i in pair_set:
    #     coeff = compute_coefficient(i)
    #     key = tuple(i[0])
    #     value = coeff * i[1]
    #     if key in result.keys():
    #         if result[key] < value:
    #             result[key] = value
    #     else:
    #         result[key] = value
    for i in pair_set:
        coeff = compute_coefficient(i)
        value = coeff * i[1]
        for key in i[0]:
            if key in result.keys():
                result[key].append(value)
            else:
                result[key] = [value]
    print result
    # return result
    return {k: max(v) for k, v in result.items()}


def main():
    sentence = []
    result = []
    cursor = dbconnect.connect()
    p = 'TM_538921269672'
    cursor.execute(
        "select comment.content from product,comment where comment.product_id = product.product_id and product.product_id = '%s'" %
        (p,))
    for c in cursor.fetchall():
        r = compute_sentiment(c[0])
        sentence.append(c[0])
        result.append(r)
    f = open("../output/sentiment/comment_sentiments.txt", 'a')
    f.truncate()
    for i, sen in enumerate(sentence):
        f.write(sen.decode('utf-8') + '\n')
        for key in result[i].keys():
            s = ''
            for a in key:
                s += ','.join(a) + ' '
            f.write(s + ':' + str(result[i][key]) + ';')
        f.write('\n\n\n')

    senti_dict = {}
    for i in result:
        for key, value in i.iteritems():
            for f in key:
                if f in senti_dict.keys():
                    senti_dict[f].append(value)
                else:
                    senti_dict[f] = [value]

    f = open('../output/sentiment/product_general.txt', 'a')
    f.truncate()
    for key, value in senti_dict.iteritems():
        f.write(','.join(key) + '  ' + str(len(value)) + '  ' + str(sum(value)/len(value)) + '\n')

    print 'finish'


def compute(platform, cat, brand, product_id=None):
    senti_dict = {}
    db = dbconnect.connect()
    c = db.cursor()
    c.execute("set names utf8")
    if product_id is None:
        sql = "select id, content from web_comment,web_product where web_comment.product_id like '%s_%%' " \
              "and web_comment.product_id = web_product.product_id and web_product.category = '%s' " \
              "and web_product.brand = '%s' and sentiment is NULL " % (platform.upper(), cat, brand)

    else:
        sql = "select id, content from web_comment where product_id = '%s' and sentiment is NULL" % product_id
    c.execute(sql)

    for i in c.fetchall():
        r = compute_sentiment(i[1])
        s = {}
        for k, v in r.items():
            s[','.join(k)] = v

        sql = 'update web_comment set sentiment = %s where id = %s'
        args = [json.dumps(s, encoding="UTF-8", ensure_ascii=False), i[0]]
        c.execute(sql, args)
        db.commit()

    if product_id is None:
        sql = "select sentiment from web_comment,web_product where web_comment.product_id like '%s_%%' " \
              "and web_comment.product_id = web_product.product_id and web_product.category = '%s' " \
              "and web_product.brand = '%s' and sentiment is not NULL" % (platform.upper(), cat, brand)
        # args = [platform.upper(), cat, brand]

    else:
        sql = "select sentiment from web_comment where product_id = '%s' and sentiment is not NULL" % product_id
        # args = [product_id]

    c.execute(sql)
    result = [item[0] for item in c.fetchall()]

    db.commit()
    c.close()
    db.close()

    for i in result:
        i = eval(i)
        for key, value in i.iteritems():
            key = key.decode("utf-8")
            if key in senti_dict.keys():
                senti_dict[key].append(value)
            else:
                senti_dict[key] = [value]
    return senti_dict, get_hierarchy_sentiment(deepcopy(senti_dict))

aspect_hierarchy = aspect_tree.build()


def get_hierarchy_sentiment(aspect_senti_dict):
    result = {}
    for high in aspect_hierarchy:
        high_str = " ".join(high)
        result[high_str] = {}
        result[high_str]['low'] = {}
        result[high_str]['count'] = 0
        result[high_str]['sum'] = 0
        result[high_str]['low'][high_str] = []
        for low in aspect_hierarchy[high]:
            result[high_str]['low'][" ".join(low)] = []
        for aspect, senti_list in aspect_senti_dict.items():
            sim = HowNet.similar_word(str("".join(high)), str("".join(aspect.split(','))))
            if sim is not None and sim > 0.9:
                result[high_str]['low'][high_str].extend(senti_list)
                result[high_str]['count'] += len(senti_list)
                result[high_str]['sum'] += sum(senti_list)
            for low in aspect_hierarchy[high]:
                sim = HowNet.similar_word(str("".join(low)), str("".join(aspect.split(','))))
                if sim is not None and sim > 0.9:
                    result[high_str]['low'][" ".join(low)].extend(senti_list)
                    result[high_str]['count'] += len(senti_list)
                    result[high_str]['sum'] += sum(senti_list)
    return result
