from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse
from flaskext.mysql import MySQL
from flask import Response
import json

app = Flask(__name__)
api = Api(app)


mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'manshinee'
app.config['MYSQL_DATABASE_DB'] = 'mansheet'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


class User(Resource):
    def post(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('username', type=str)
            parser.add_argument('password', type=str)
            args = parser.parse_args()

            _Uname = args['username']
            _Password = args['password']

            #닉네임 형식 확인
            if (_Uname[2].isspace()) or (not (_Uname[0:2].isdigit())) or (len(_Uname)>10):
                res = {'Message': "Please check your nickname. \nFirst two character must be digit. \nDo not write off digits and nickname.\nNickname must be less than 10 characters"}
                return Response(str(res).replace("'", "\""), status=406, mimetype='application/json')

            #비밀번호가 너무 짧거나 길지 않은지 확인
            if (len(_Password)<4) :
                res = {'Message': "Password is too short. It must be longer than 4 characters"}
                return Response(str(res).replace("'", "\""), status=406, mimetype='application/json')
            if (len(_Password)>40) :
                res = {'Message': "Password is too long. It must be less than 40 characters"}
                return Response(str(res).replace("'", "\""), status=406, mimetype='application/json')

            #이미 있는 유저의 아이디인지 확인
            conn = mysql.connect()
            cursor = conn.cursor()
            sql = """select exists (select 1 from MUSER where Uname = '""" + _Uname + """');"""
            cursor.execute(sql)
            already = cursor.fetchone()[0]
            if already :
                res = {'Message': "User already exists"}
                return Response(str(res).replace("'", "\""), status=406, mimetype='application/json')

            #db에 유저 insert
            sql = """insert into MUSER values ('""" + _Uname + """', '""" + _Password + """');"""
            cursor.execute(sql)
            conn.commit()

            #유저의 default 그룹 생성
            sql = """INSERT INTO MGROUP(Gname, Default_group, Owner_uname) 
                    VALUES ( '""" + _Uname + """의 일정' , 'Y', '""" + _Uname + """');"""
            cursor.execute(sql)
            conn.commit()

            #유저가 default 그룹에 들어가있다는 관계 추가
            sql = """SELECT last_insert_id();"""
            cursor.execute(sql)
            last_insert_id = cursor.fetchone()[0] #fetchone은 1차원 튜플, fetchall은 2차원
            sql = """INSERT INTO PARTICIPATE 
                    VALUES ( '""" + _Uname + """' ,
                            """ + str(last_insert_id) + """);"""
            cursor.execute(sql)
            conn.commit()

            res = {'Message': "User created successfully. \nGo to mainpage for log-in"}
            return Response(str(res).replace("'", "\""), status=201, mimetype='application/json')

        except Exception as e:
            return Response(str({'error': str(e)}), status=400, mimetype="application/json")

    def delete(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('username', type=str)
            parser.add_argument('password', type=str)
            args = parser.parse_args()

            _Uname = args['username']
            _Password = args['password']

            #이미 있는 유저의 아이디인지 확인
            conn = mysql.connect()
            cursor = conn.cursor()
            sql = """select * from MUSER where Uname = '""" + _Uname + """';"""
            cursor.execute(sql)
            existing = cursor.fetchone()

            if existing is None: #존재하지 않는 아이디인 경우
                res = {'Message': "User does not exists"}
                return Response(str(res).replace("'", "\""), status=406, mimetype='application/json')
            if existing[1] != _Password: #옳지 않은 비밀번호를 입력한 경우
                res = {'Message': "Please enter right password for secession"}
                return Response(str(res).replace("'", "\""), status=406, mimetype='application/json')

            #유저 삭제
            sql = """delete from SCHEDULE where Uname = '""" + _Uname + """';"""
            cursor.execute(sql)
            conn.commit()
            sql = """delete from PARTICIPATE where Uname = '""" + _Uname + """';"""
            cursor.execute(sql)
            conn.commit()
            sql = """delete from MGROUP where Owner_uname = '""" + _Uname + """';"""
            cursor.execute(sql)
            conn.commit()
            sql = """delete from MUSER where Uname = '""" + _Uname + """';"""
            cursor.execute(sql)
            conn.commit()
            res = {'Message': "User deleted successfully. \nGo to mainpage for log-in"}
            return Response(str(res).replace("'", "\""), status=200, mimetype='application/json')

        except Exception as e:
            return Response(str({'error': str(e)}), status=400, mimetype="application/json")

    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('username', type=str)
            parser.add_argument('password', type=str)
            args = parser.parse_args()

            _Uname = args['username']
            _Password = args['password']

            #이미 있는 유저의 아이디인지 확인
            conn = mysql.connect()
            cursor = conn.cursor()
            sql = """select * from MUSER where Uname = '""" + _Uname + """';"""
            cursor.execute(sql)
            existing = cursor.fetchone()

            if existing is None: #존재하지 않는 아이디인 경우
                res = {'Message': "User does not exists"}
                return Response(str(res).replace("'", "\""), status=406, mimetype='application/json')
            if existing[1] != _Password: #옳지 않은 비밀번호를 입력한 경우
                res = {'Message': "Please enter right password for log-in"}
                return Response(str(res).replace("'", "\""), status=406, mimetype='application/json')

            #로그인 된 유저의 디폴트 그룹의 GID 가져오기
            conn = mysql.connect()
            cursor = conn.cursor()
            sql = """select * from MGROUP where Owner_uname = '""" + _Uname + """' and Default_group = 'Y';"""
            cursor.execute(sql)
            defaultgid = cursor.fetchone()[0]

            #로그인 된 유저의 디폴트 그룹에 해당하는 개인 스케쥴 모두 쿼리
            sql = """select * from SCHEDULE where Uname = '""" + _Uname + """' and Gid = """ + str(defaultgid) + """;"""
            cursor.execute(sql)
            row_headers=[x[0] for x in cursor.description]
            schedules = cursor.fetchall()

            json_data=[]
            for one in schedules:
                json_data.append(dict(zip(row_headers,one)))
            return Response(str(json_data).replace("'", "\""), status=200, mimetype='application/json')

        except Exception as e:
            return Response(str({'error': str(e)}), status=400, mimetype="application/json")

api.add_resource(User, '/user')

if __name__ == '__main__':
    app.run(debug=True)


