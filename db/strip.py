import dbconnect


def main():
    c = dbconnect.connect()
    c.execute("select id, good, bad, summary, user, helpless from pos_neg1")
    for i in c.fetchall():
        id = i[0]
        good = i[1].strip().replace("\n", "")
        bad = i[2].strip().replace("\n", "")
        summary = i[3].strip().replace("\n", "")
        user = i[4].strip()
        helpless = i[5].strip()[10:-1]
        # print helpless[10:-1]
        sql = 'update pos_neg1 set good = "%s", bad = "%s", summary = "%s", user = "%s", helpless ="%s" where id = %s' %\
              (good, bad, summary, user, helpless, id)
        # print sql
        try:
            c.execute(sql)
        except Exception, e:
            print sql

main()
