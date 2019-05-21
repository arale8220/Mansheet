from flask import Flask
from flask_restful import Resource, Api
from flask_restful import reqparse
from flaskext.mysql import MySQL
from flask import Response
from flask_cors import CORS, cross_origin
import json

app = Flask(__name__)
api = Api(app)

CORS(app, origins="*")

mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = 'admin'
app.config['MYSQL_DATABASE_PASSWORD'] = 'manshinee'
app.config['MYSQL_DATABASE_DB'] = 'mansheet'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


class USER(Resource):
    @cross_origin()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)
        args = parser.parse_args()

        _Uname = args['username']
        _Password = args['password']
        #닉네임 형식 확인
        if (len(_Uname)<4) or (not (_Uname[0:2].isdigit())) or (len(_Uname)>10) or (_Uname[2].isspace()) :
            return bad406Response("Please check your nickname. \nFirst two character must be digit. \nDo not write off digits and nickname.\nNickname must be less than 10 characters")
            
        #비밀번호가 너무 짧거나 길지 않은지 확인
        if (len(_Password)<4) :
            return bad406Response("Password is too short. It must be longer than 4 characters")
        if (len(_Password)>40) :
            return bad406Response("Password is too long. It must be less than 40 characters")
        
        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            #이미 있는 유저의 아이디인지 확인
            sql = """select exists (select 1 from MUSER where Uname = '""" + _Uname + """');"""
            cursor.execute(sql)
            already = cursor.fetchone()[0]
            if already :
                return bad406Response("User already exists")

            #유저 추가 프로시져 실행
            args = (_Uname, _Password, 0)
            result_args = cursor.callproc('createMuser', args)
            cursor.execute('SELECT @_createMuser_2') 
            result = cursor.fetchone()
            if result[0]:
                return user20XResponse("User created successfully. \nGo to mainpage for log-in", \
                        _Uname, _Password, 201)
            else:
                raise SQLError()

        except Exception as e:
            return error400Response(str(e))

        finally:
            cursor.close()
            conn.close()


    @cross_origin()
    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)
        args = parser.parse_args()

        _Uname = args['username']
        _Password = args['password']

        try:
            #이미 있는 유저의 아이디인지 확인
            conn = mysql.connect()
            cursor = conn.cursor()
            sql = """select * from MUSER where Uname = '""" + _Uname + """';"""
            cursor.execute(sql)
            existing = cursor.fetchone()

            if (existing is None): #존재하지 않는 아이디인 경우
                return bad406Response("User does not exists")    
            if existing[1] != _Password: #옳지 않은 비밀번호를 입력한 경우
                return bad406Response("Please enter right password for secession")
                
            #유저 삭제 프로시져 실행
            args = [_Uname, _Password, 0]
            result_args = cursor.callproc('deleteMuser', args)
            cursor.execute('SELECT @_deleteMuser_2') 
            result = cursor.fetchone()
            if result[0]:
                return user20XResponse("User deleted successfully. \nGo to mainpage for log-in", \
                        _Uname, _Password, 200)
            else:
                raise SQLError()

        except Exception as e:
            return error400Response(str(e))

        finally:
            cursor.close()
            conn.close()
    
    @cross_origin()
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        parser.add_argument('password', type=str)
        args = parser.parse_args()

        _Uname = args['username']
        _Password = args['password']

        try:
            #이미 있는 유저의 아이디인지 확인
            conn = mysql.connect()
            cursor = conn.cursor()
            sql = """select * from MUSER where Uname = '""" + _Uname + """';"""
            cursor.execute(sql)
            existing = cursor.fetchone()

            if (existing is None): #존재하지 않는 아이디인 경우
                return bad406Response("User does not exists")    
            if existing[1] != _Password: #옳지 않은 비밀번호를 입력한 경우
                return bad406Response("Please enter right password for secession")
            
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

            res = {'message' : "User logged in successfully.", \
                'username' : _Uname, 'password' : _Password, \
                'schedules' : json_data}

            return Response(str(res).replace("'", "\""), status=200, mimetype='application/json')

        except Exception as e:
            return error400Response(str(e))

        finally:
            cursor.close()
            conn.close()

class GROUP(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        parser.add_argument('groupname', type=str)
        parser.add_argument('entries')
        args = parser.parse_args()

        _Uname = args['username']
        _Gname = args['groupname']
        _Entries = args['entries']

        #그룹 이름 길이 확인
        if (len(_Uname)<1):
            return bad406Response("Group name is too short")
        if (len(_Uname)>30):
            return bad406Response("Group name is too long")

        try:
            #그룹 추가
            conn = mysql.connect()
            cursor = conn.cursor()
            args = [_Uname, _Gname, 0]
            result_args = cursor.callproc('createMgroup', args)
            cursor.execute('SELECT @_createMgroup_2, @_createMgroup_3') 
            result = cursor.fetchone()
            if result[0]:
                res = {'message': "Group created successfully.", 'ownername':_Uname, 'groupname':_Gname}
                for i in _Entries:
                    cursor.execute("""INSERT INTO PARTICIPATE VALUES ('"""+i['username']+"""', """ + result[1] + """');""")
############3
                    return Response(str(res).replace("'", "\""), status=201, mimetype='application/json')
            else:
                return bad406Response("Please check that you already have group with same name")

        except Exception as e:
            return error400Response(str(e))
        
        finally:
            cursor.close()
            conn.close()

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('groupname', type=str)
        args = parser.parse_args()

        _Gname = args['groupname']

        try:
            #그룹 id 가져오기
            conn = mysql.connect()
            cursor = conn.cursor()

            args = [_Gname, 0, 0]
            result_args = cursor.callproc('getMgroup', args)
            cursor.execute('SELECT @_createMgroup_1, @_createMgroup_2') 
            result = cursor.fetchone()

            if result[0]:
                cursor.execute("""select Uname from PARTICIPATE where Gid = '""" + result[1] + """";""" ) 
                users = cursor.fetchall()
                json_data = []
                for user in users:
                    content = {'username': user[0]}
                    json_data.append(content)

############


                group_data = {  'groupname':_Gname,\
                                'ownername':ownername,\
                                'entries':json_data,\
                                'schedules':schedules}
                return Response(str(group_data).replace("'", "\""), status=200, mimetype='application/json')










                res = {'message': "Group created successfully.", 'ownername':_Uname, 'groupname':_Gname}
                for i in _Entries:
                    cursor.execute("""INSERT INTO PARTICIPATE VALUES ('"""+i['username']+"""', """ + result[1] + """');""") 
                return Response(str(res).replace("'", "\""), status=201, mimetype='application/json')
            else:
                return bad406Response("Please check that you already have group with same name")

        except Exception as e:
            return error400Response(str(e))
        
        finally:
            cursor.close()
            conn.close()

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        parser.add_argument('groupname', type=str)
        args = parser.parse_args()

        _Uname = args['username']
        _Gname = args['groupname']

        try:
            #이미 있는 유저의 그룹인지 확인
            conn = mysql.connect()
            cursor = conn.cursor()
            sql = """select * from MGROUP where Owner_uname = '""" + _Uname + """' AND Gname = '"""+ _Gname +"""' ;"""
            cursor.execute(sql)
            existing = cursor.fetchone()

            if (existing is None): #존재하지 않는 아이디인 경우
                return bad406Response("Group of that name does not exists")
                
            #그룹 삭제 프로시져 실행
            args = [existing[0], 0]
            result_args = cursor.callproc('deleteMuser', args)
            cursor.execute('SELECT @_deleteMuser_1') 
            result = cursor.fetchone()
            if result[0]:
                return Response(str({'message':"Group deleted successfully."}).replace("'", "\""), status=200, mimetype='application/json')
            else:
                raise SQLError()

        except Exception as e:
            return error400Response(str(e))

        finally:
            cursor.close()
            conn.close()


class ALLUSER(Resource):
    def get(self):
        try:
            parser = reqparse.RequestParser()
            parser.add_argument('username', type=str)
            args = parser.parse_args()
            _Uname = args['username']

            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("""select Uname from MUSER where Uname <> '""" + _Uname + """";""" ) 
            rv = cursor.fetchall()
            alluser = []
            for result in rv:
                content = {'username': result[0]}
                payload.append(content)
            return Response(str(alluser).replace("'", "\""), status=200, mimetype='application/json')

        except Exception as e:
            return error400Response(str(e))
        
        finally:
            cursor.close()
            conn.close()

class ALLGROUOP(Resource):
    def get(self):
        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("select Gid, Gname from MGOUP where Default_group='N';" ) 
            rv = cursor.fetchall()
            alluser = []
            row_headers=[x[0] for x in cursor.description] 
            rv = cursor.fetchall()
            json_data=[]
            for result in rv:
                json_data.append(dict(zip(row_headers,result)))
            return Response(str(json_data).replace("'", "\""), status=200, mimetype='application/json')

        except Exception as e:
            return error400Response(str(e))
        
        finally:
            cursor.close()
            conn.close()


        

api.add_resource(USER, '/user')
api.add_resource(GROUP, '/group')
api.add_resource(ALLUSER, '/alluser')
api.add_resource(ALLGROUOP, '/allgroup')


def bad406Response(msg):
    return Response(str({'message': msg}).replace("'", "\""), status=406, mimetype='application/json')

def user20XResponse(msg, user, pw, state):
    res = {'message' : msg, 'username' : user, 'password' : pw}
    return Response(str(res).replace("'", "\""), status=state, mimetype='application/json')

def error400Response(msg):
    return Response(str({'error': msg}), status=400, mimetype="application/json")

class SQLError(Exception):
    def __str__(self):
        return "There are some problem in SQL. It has been rolled back."

if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)


