from flask import Flask, render_template, redirect, url_for, request
import pymysql

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('index.html')

# url for select
@app.route("/select")
def select():
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
            sql = "SELECT * FROM EMPLOYEE;"
            # Execute SQL
            cursor.execute(sql)

            # Fetch the result
            # result is dictionary type
            result = cursor.fetchall()
            # Print tuples

            output = ""
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
                         user='root',
                         passwd='1111',
                         db='cs360',
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
    app.run('0.0.0.0', port=5000)
