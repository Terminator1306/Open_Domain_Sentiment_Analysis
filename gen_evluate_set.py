from sentiment_analysor import sentiment1
import MySQLdb
import json

db = MySQLdb.connect("127.0.0.1", "root", "", "tmall")
db.set_character_set('utf8')
c = db.cursor()
c.execute("set names utf8")
# c.execute("select bad from pos_neg1 where LENGTH (bad) < 120 and LENGTH(bad) > 0 limit 4500, 6500")
c.execute("select content from comment where LENGTH (content) > 0 and LENGTH (content)< 120 limit 7500,9500")

mdb = MySQLdb.connect("127.0.0.1", "root", "", "gp_web")
mdb.set_character_set('utf8')
c1 = mdb.cursor()
c1.execute("set names utf8")
index = 6950
for i in c.fetchall():
    s = {}
    bad_list = []
    good_list = []
    r = sentiment1.compute_sentiment(i[0], "phone")
    for k, v in r.items():
        s[','.join(k)] = v
    for k in s.keys():
        v = s[k]
        if v < 0:
            bad_list.append(k)
        if v > 0:
            good_list.append(k)
    sql = 'insert into evaluation(id, content, sentiment, bad, good) VALUES (%s, %s, %s,%s,%s)'
    args = [str(index), i[0], json.dumps(s, encoding="UTF-8", ensure_ascii=False), " ".join(bad_list), " ".join(good_list)]
    c1.execute(sql, args)
    mdb.commit()
    index += 1
print "finish"
