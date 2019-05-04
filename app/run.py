from flask import Flask, render_template, redirect, url_for, request
import pymysql

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')


@app.route("/signup", methods = ['POST', 'GET'])
def signup():
    if request.method == 'POST':
        uname = request.form['Uname']
        password = request.form['Password']

        # Connect to database
        db = pymysql.connect(host='localhost',
                             port=3306,
                             user='admin',
                             passwd='manshinee',
                             db='mansheet',
                             charset='utf8')

        try:
            with db.cursor() as cursor:
                sql = """INSERT INTO MUSER
                         VALUES('""" + Uname + """',
                                '""" + Password + """');"""
                cursor.execute(sql)
            db.commit()
            signupres = "회원가입이 성공적으로 완료되었습니다 \n환영합니다!"

        except:
            signupres = "회원가입에 실패하였습니다. \n이미 해당 닉네의 사용자가 존재합니다"

        finally:
            db.close()
        return render_template("signupres.html", signupRes = signupres)

    else :
        return render_template('signup.html')



@app.route("/login", methods = ['POST', 'GET'])
def login():
    if request.method == 'POST':
        uname = request.form['Uname']
        password = request.form['Password']
        
        # Connect to database
        db = pymysql.connect(host='localhost',
                             port=3306,
                             user='admin',
                             passwd='manshinee',
                             db='mansheet',
                             charset='utf8')

        try:
            with db.cursor() as cursor:
                sql = """select * from MUSER where Uname like '""" + uname + """';"""
                cursor.execute(sql)
                row = cursor.fetchone()


                if ((uname != row[0]) or (password != row[1])) : 
                    signupres = "로그인에 실패하였습니다. \n아이디와 비밀번호를 다시 한번 확인해주세요...\n 지금 값은 {0}".format(row)
            
                else : 
                    signupres = "로그인 돼따 슈바"
                return render_template("signupres.html", signupRes = signupres)
                    #raise ValueError

            redirect(url_for("select"))

        #except:

        finally:
            db.close()
    else :
        return render_template('login.html')


# url for select
@app.route("/select")
def select():
    
    try:
        # Set cursor to the database
        with db.cursor() as cursor:
            # Write SQL query
            sql = "SELECT * FROM MUSER;"
            # Execute SQL
            cursor.execute(sql)

            # Fetch the result
            # result is dictionary type
            result = cursor.fetchall()
            # Print tuples

            output = ""
            for row in result:
                output += "{0} {1}\n".format(row[0], row[2])

            # Set cursor to the database
        with db.cursor() as cursor:
            # Write SQL query
            sql = "SELECT * FROM MGROUP;"
            # Execute SQL
            cursor.execute(sql)

            # Fetch the result
            # result is dictionary type
            result = cursor.fetchall()
            # Print tuples
            for row in result:
                output += "{0} {1}\n".format(row[0], row[2])


    finally:
        db.close()

    return render_template('select.html', result=output)

@app.route("/redirect_insert")
def redirect_insert():
    return render_template('insert.html')

@app.route("/insert", methods = ['POST'])
def insert():
    if request.method == 'POST':
        fname = request.form['FirstName']
        lname = request.form['LastName']
        ssn = request.form['Ssn']
        return redirect(url_for('insert_sent', Fname = fname, Lname = lname, Ssn = ssn))

@app.route("/insert_sent/<Fname>/<Lname>/<Ssn>")
def insert_sent(Fname, Lname, Ssn):
    
    # Connect to database
    db = pymysql.connect(host='localhost',
                         port=3306,
                         user='admin',
                         passwd='manshinee',
                         db='mansheet',
                         charset='utf8')

    try:
        # Set cursor to the database
        with db.cursor() as cursor:
            # Write SQL query
            sql = """INSERT INTO EMPLOYEE
                     VALUES('""" + Fname + """',
                            'E','"""\
                            + Lname + "','"\
                            + Ssn + """',
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
    finally:
        db.close()

    return redirect("/")

if __name__ == "__main__":
    app.run('35.200.11.18', port=5000)
