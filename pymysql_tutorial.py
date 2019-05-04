import pymysql

# Connect to database
db = pymysql.connect(host='localhost',
                     port=3306,
                     user='root',
                     passwd='1111',
                     db='cs360',
                     charset='utf8')

try:
    # Set cursor to the database
    with db.cursor() as cursor:
        # Write SQL query
        sql = """INSERT INTO EMPLOYEE
                 VALUES('James',
                        'E',
                        'Borg',
                        '888665555',
                        '1937-11-10',
                        '450 Stone, Houston, TX',
                        'M',
                        55000,
                        NULL,
                        1);"""
        # Execute SQL
        cursor.execute(sql)
    # You must manually commit after every DML methods.
    db.commit()

    # Set cursor to the database
    with db.cursor() as cursor:
        # Write SQL query
        sql = "SELECT * FROM EMPLOYEE;"
        # Execute SQL
        cursor.execute(sql)

        # Fetch the result
        # result is dictionary type
        result = cursor.fetchall()
        # Print tuples
        print("---Employee name---")
        for row in result:
            print('{0} {1}'.format(row[0], row[2]))
finally:
    db.close()
