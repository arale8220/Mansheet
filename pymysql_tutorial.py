import pymysql

# Connect to database
db = pymysql.connect(host='127.0.0.1',
                     port=3306,
                     user='admin',
                     passwd='manshinee',
                     db='mansheet',
                     charset='utf8')

try:
    with db.cursor() as cursor:
        sql = """INSERT INTO MUSER
                 VALUES('11아리',
                        'arale');"""
        cursor.execute(sql)
    
    db.commit()

    with db.cursor() as cursor:
        sql = """INSERT INTO MGROUP(Gname,
                                    Default_group,
                                    Owner_uname)
                 VALUES('11아리의 개인일정',
                        1,
                        '11아리');"""
        cursor.execute(sql)

    db.commit()

    with db.cursor() as cursor:
        sql = "SELECT * FROM MGROUP;"
        cursor.execute(sql)
        result = cursor.fetchall()
        # Print tuples
        print("---GROUP name---")
        for row in result:
            print('{0} {1}'.format(row[1], row[3]))
finally:
    db.close()
