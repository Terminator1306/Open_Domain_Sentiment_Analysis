# coding=utf-8
from sentiment_analysor import sentiment1
import MySQLdb
import json


def compute_sentiment():
    db = MySQLdb.connect("127.0.0.1", "root", "", "gp_web")
    db.set_character_set('utf8')
    c = db.cursor()
    c.execute("set names utf8")
    c.execute("select id, content from evaluation")
    for i in c.fetchall():
        s = {}
        r = sentiment1.compute_sentiment(i[1], "phone")
        for k, v in r.items():
            s[','.join(k)] = v

        sql = 'update evaluation set sentiment = %s where id = %s'
        args = [json.dumps(s, encoding="UTF-8", ensure_ascii=False), i[0]]
        c.execute(sql, args)
        db.commit()


def evaluate():
    TP = FP = TN = FN = 0
    FP1 = FN1 = FP2 = FN2 = 0
    exceed = miss = count = 0
    good_count = 0
    bad_count = 0
    all_set = set([])
    good_set = set([])
    bad_set = set([])
    db = MySQLdb.connect("127.0.0.1", "root", "", "gp_web")
    db.set_character_set('utf8')
    c = db.cursor()
    c.execute("set names utf8")
    c.execute("select sentiment, good, bad from evaluation")
    for i in c.fetchall():
        good = []
        bad = []
        hit = 0
        result = json.loads(i[0])
        for g in i[1].split(" "):
            if len(g) > 0:
                good.append(tuple(g.split(",")))
        for b in i[2].split(" "):
            if len(b) > 0:
                bad.append(tuple(b.split(",")))

        key_list = []
        for key in result:
            k = tuple(key.split(","))
            key_list.append(k)
            if result[key] > 0:
                if k in good:
                    TP += 1
                    hit += 1
                elif k in bad:
                    FN += 1
                    hit += 1
                else:
                    FP2 += 1
                    exceed += 1
            elif result[key] < 0:
                if k in good:
                    FP += 1
                    hit += 1
                elif k in bad:
                    TN += 1
                    hit += 1
                else:
                    FN2 += 1
                    exceed += 1

        for g in good:
            if g not in key_list:
                FN1 += 1
        for b in bad:
            if b not in key_list:
                FP1 += 1

        count += len(bad) + len(good)
        miss += len(bad) + len(good) - hit
        bad_count += len(bad)
        good_count += len(good)
        all_set = all_set | set(bad) | set(good)
        bad_set = bad_set | set(bad)
        good_set = good_set | set(good)

    FN += FN1 + FN2
    FP += FP1 + FP2

    P = float(TP) / (TP + FP)
    ACC = (float(TP) + float(TN)) / (TP + FP + TN + FN)
    R = float(TP) / (TP + FN)
    F1 = 2 * float(TP) / (2 * TP + FP + FN)

    print "TP, FP, TN, FN"
    print TP, FP, TN, FN
    print "FP1, FN1"
    print FP1, FN1
    print "FP2, FN2"
    print FP2, FN2
    print 'P:', P
    print 'ACC:', ACC
    print "R:", R
    print "F1:", F1
    print "beyond:", exceed, 1 - float(exceed)/count
    print "miss:", miss, 1 - float(miss)/count
    print "total count:", count
    print len(all_set), len(bad_set), len(good_set)
    print good_count, bad_count

if __name__ == '__main__':
    # compute_sentiment()
    evaluate()
