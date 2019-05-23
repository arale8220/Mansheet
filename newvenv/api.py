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
            cursor.callproc('createMuser', args)
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

        return error400Response("Check the json data you send.")


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
            args = (_Uname, _Password, 0)
            cursor.callproc('deleteMuser', args)
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

        return error400Response("Check the json data you send.")
    
    @cross_origin()
    def patch(self):
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

            '''
            #로그인 된 유저의 디폴트 그룹에 해당하는 개인 스케쥴 모두 쿼리
            sql = """select * from SCHEDULE where Uname = '""" + _Uname + """' and Gid = """ + str(defaultgid) + """;"""
            cursor.execute(sql)
            row_headers=[x[0] for x in cursor.description]
            schedules = cursor.fetchall()

            json_data=[]
            for one in schedules:
                json_data.append(dict(zip(row_headers,one)))
            '''

            res = {'message' : "User logged in successfully.", \
                'username' : _Uname, 'password' : _Password, \
                'defaultgid' : defaultgid}

            return Response(str(res).replace("'", "\""), status=200, mimetype='application/json')

        except Exception as e:
            print(e)
            return error400Response(str(e))

        finally:
            cursor.close()
            conn.close()

        return error400Response("Check the json data you send.")

class GROUP(Resource):
    @cross_origin()
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        parser.add_argument('groupname', type=str)
        parser.add_argument('entries', action='append')
        args = parser.parse_args()

        _Uname = args['username']
        _Gname = args['groupname']
        _Entries = args['entries']

        #그룹 이름 길이 확인
        if (len(_Uname)<1):
            return bad406Response("Group name is too short")
        if (len(_Uname)>30):
            return bad406Response("Group name is too long")
        if (_Entries is None):
            return bad406Response("There is no entries in json body")


        try:
            #그룹 추가
            conn = mysql.connect()
            cursor = conn.cursor()
            args = (_Uname, _Gname, 0, 0)
            cursor.callproc('createMgroup', args)
            cursor.execute('SELECT @_createMgroup_2, @_createMgroup_3') 
            result = cursor.fetchone()

            if result[0]:
                json_schedules = []
                condition_str = "Gid = " + str(result[1])
                add_str = " or Uname = '"

                _Entries_return = []
                for i in _Entries:
                    i=json.loads(i.replace("'", "\""))
                    _Entries_return.append(i)
                    cursor.execute("INSERT INTO PARTICIPATE VALUES ('" + i['username']+"""', """ + str(result[1]) + """);""")
                    conn.commit()
                    condition_str += add_str + i['username'] + "'"

                condition_str += add_str + _Uname + "'"
                sql = "SELECT * FROM SCHEDULE WHERE " + condition_str + ";"
                cursor.execute(sql)
                row_headers=('sid', 'start_date', 'start_time', 'duration', 'description', 'username', 'groupid')
                schedules = cursor.fetchall()
                for one in schedules:
                    cursor.execute("SELECT Gname FROM MGROUP WHERE Gid = " + str(one[6]) + ";")
                    tempGname = cursor.fetchone()[0]
                    tempJson = dict(zip(row_headers,one))
                    tempJson.update({'groupname': tempGname})
                    json_schedules.append(tempJson)

                res = {'message': "Group created successfully.", \
                        'ownername':_Uname, 'groupname':_Gname, 'groupid' : result[1], \
                        'schedules' : json_schedules, \
                        'entries' : _Entries_return}

                return Response(str(res).replace("'", "\""), status=201, mimetype='application/json')
            
            else:
                return bad406Response("Group did not be created. \nPlease check that you make group with undefined user, and group with same name already exists")

        except Exception as e:
            return error400Response(str(e))
        
        finally:
            cursor.close()
            conn.close()

        return error400Response("Check the json data you send.")

    @cross_origin()
    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument('groupname', type=str)
        args = parser.parse_args()

        _Gname = args['groupname']

        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            #그룹 id, 오너 이름 가져오기
            sql = """SELECT Gid, Owner_uname FROM MGROUP WHERE Gname = '""" + _Gname + """';"""
            cursor.execute(sql)
            existing = cursor.fetchone()
            _Gid = existing[0]
            _Owner = existing[1]

            #그룹 엔트리 가져오기
            sql = """SELECT Uname FROM PARTICIPATE WHERE Gid = """ + str(_Gid) + \
                    """ and Uname <> '""" + _Owner + """';"""
            cursor.execute(sql)
            _Entries = []
            condition_str = "Gid = " + str(_Gid)
            add_str = " or Uname = '"
            schedules = cursor.fetchall()
            for one in schedules:
                _Entries.append({"username" : one[0]})
                condition_str += add_str + one[0] + "'"

            #그룹의 스케쥴, 엔트리의 개인 스케쥴, 오너의 개인 스케줄 가져오기
            condition_str += add_str + _Owner + "'"
            sql = "SELECT * FROM SCHEDULE WHERE " + condition_str + ";"
            cursor.execute(sql)
            row_headers=('sid', 'start_date', 'start_time', 'duration', 'description', 'username', 'groupid')
            _Schedules = []
            schedules = cursor.fetchall()
            for one in schedules:
                cursor.execute("SELECT Gname FROM MGROUP WHERE Gid = " + str(one[6]) + ";")
                tempGname = cursor.fetchone()[0]
                tempJson = dict(zip(row_headers,one))
                tempJson.update({'groupname': tempGname})
                _Schedules.append(tempJson)

            #결과 정리
            result = {
                        "message" : "Group information fetched.",
                        "ownername" : _Owner,
                        "groupname" : _Gname,
                        "groupid" : _Gid,
                        "schedules" : _Schedules,
                        "entries" : _Entries
                    }

            return Response(str(result).replace("'", "\""), status=200, mimetype='application/json')

        except Exception as e:
            return error400Response(str(e))
        
        finally:
            cursor.close()
            conn.close()

        return error400Response("Check the json data you send.")

    @cross_origin()
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
            sql = """select * from MGROUP where Gname = '"""+ _Gname +"""' ;"""
            cursor.execute(sql)
            existing = cursor.fetchone()

            if (existing is None): #존재하지 않는 아이디인 경우
                return bad406Response("Group of that name does not exists")
            if (_Uname == ""): #그룹의 오너와 다른 아이디인 경우
                return bad406Response("You are not the TOP of this group")
                
            #그룹 삭제 프로시져 실행
            args = [existing[0], 0]
            cursor.callproc('deleteMuser', args)
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
    @cross_origin()
    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        args = parser.parse_args()
        _Uname = args['username']

        try:
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("""SELECT Uname from MUSER where Uname <> '""" + _Uname + """';""" ) 
            rv = cursor.fetchall()
            _Alluser = []
            for result in rv:
                content = {'username': result[0]}
                _Alluser.append(content)
            return Response(str(_Alluser).replace("'", "\""), status=200, mimetype='application/json')

        except Exception as e:
            return error400Response(str(e))
        
        finally:
            cursor.close()
            conn.close()

class ALLGROUOP(Resource):
    @cross_origin()
    def patch(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str)
        args = parser.parse_args()
        _Uname = args['username']

        try:
            conn = mysql.connect()
            cursor = conn.cursor()

            #유저가 엔트리나 탑으로 들어가있는 그룹들의 아이디 구하기 => 그 아이디들이 아닌 것들 컨디션으로 저장
            cursor.execute("SELECT Gid from PARTICIPATE where Uname='" + _Uname + "';" ) 
            rv = cursor.fetchall()
            condition_str = "Default_group = 'N'"
            for i in rv:
                condition_str += " and Gid <> " + str(i[0])

            #이미 있는 그룹과 디폴트인 그룹을 제외한 그룹들에서 오너, 그룹아이디, 그룹 이름 가져오기
            cursor.execute("SELECT Gid, Gname, Owner_uname from MGROUP where " + condition_str + ";" ) 
            rv = cursor.fetchall()
            result = []
            for i in rv:
                _Owner = i[2]
                _Gname = i[1]
                _Gid = i[0]
                
                #필요한 그룹의 엔트리들 가져오기
                cursor.execute("SELECT Uname from PARTICIPATE where Gid = " + str(_Gid) + " and Uname <> '" + _Owner + "';" ) 
                entries = cursor.fetchall()
                _Entries = []
                for j in entries:
                    _Entries.append({'username' : j[0]})

                json_data = { "ownername" : _Owner,\
                        "groupname" : _Gname,\
                        "groupid" : _Gid,\
                        "entries" : _Entries }
                result.append(json_data)

            return Response(str(result).replace("'", "\""), status=200, mimetype='application/json')

        except Exception as e:
            return error400Response(str(e))
        
        finally:
            cursor.close()
            conn.close()


# mysql> insert into muser (uname, password) values ("13dd", "1234");
# mysql> insert into mgroup (gname, owner_uname) Values ("2-on", "13dd");


class SCHEDULE(Resource):
    #post -> 데이터 만들기
    #create 후 sid 만들기   
    def post(self):
         # POST = 1

        parser = reqparse.RequestParser()
        parser.add_argument('start_date', type=str)
        parser.add_argument('start_time', type=str)
        parser.add_argument('username', type=str)
        parser.add_argument('groupname',type=str)
        parser.add_argument('description', type=str)
        parser.add_argument('duration', type=str)
        args = parser.parse_args()

        _startDate = args['start_date']
        _startTime = args['start_time']
        _Gname = args['groupname']
        _Uname = args['username']
        _Description = args['description'] or ''
        _Duration = args['duration']

        try:

            #StartTime 길이 확인
            if (len(_startDate)<1) or (len(_startDate)>10):
                res = {'message': "Start date is too short or too long"}
                return Response(str(res).replace("'", "\""), status=406, mimetype='application/json')

            #그룹 추가
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("""select gid from MGROUP where Gname = '""" + _Gname + """';""" ) 
            fetchGid = cursor.fetchone()
            if fetchGid and fetchGid[0]:
                sql = """INSERT INTO SCHEDULE(Start_date,start_time,Uname,duration, Gid, description) 
                    VALUES ( '""" + _startDate + """' , '""" + _startTime + """','""" + _Uname + """','""" + str(_Duration) + """', '""" + str(fetchGid[0]) + """', '""" + _Description + """');"""
            else :
                res = {'message': "No such group exists"}
                return Response(str(res).replace("'", "\""), status=201, mimetype='application/json')
            cursor.execute(sql)
            conn.commit()

            res = {'message': "schedule created successfully."}
            return Response(str(res).replace("'", "\""), status=201, mimetype='application/json')

        except Exception as e :
            print(e)
            return error400Response(str(e))

        finally:
            cursor.close()
            conn.close()
    #update 시간표. Description 바꾸기
    def patch(self):
        try:
            #과연 다른 정보들이 필요한가? Sid만 주면 안되남
            parser = reqparse.RequestParser()
            parser.add_argument('start_date', type=str)
            parser.add_argument('start_time', type=str)
            parser.add_argument('username', type=str)
            parser.add_argument('groupname',type=str)
            parser.add_argument('description', type=str)
            parser.add_argument('duration', type=str)
            parser.add_argument('sid', type=str)
            args = parser.parse_args()

            _startDate = args['start_date']
            _startTime = args['start_time']
            _Gname = args['groupname']
            _Uname = args['username']
            _Description = args['description'] or ''
            _Duration = args['duration']
            _Sid= args['sid']

            #그룹 추가
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("""select Gid from SCHEDULE where Sid = '""" + str(_Sid) + """';""" ) 
            fetchGid = cursor.fetchone()

            print(fetchGid[0])

            if (fetchGid[0]):
                sql = """DELETE FROM SCHEDULE where Sid = '""" + str(_Sid) + """';"""
            else :
                res = {'message': "schedule does not exists "}
                return Response(str(res).replace("'", "\""), status=406, mimetype='application/json')
            cursor.execute(sql)
            sql = """INSERT INTO SCHEDULE(Start_date,start_time,Uname,duration, Gid, description) 
                    VALUES ( '""" + _startDate + """' , '""" + _startTime + """','""" + _Uname + """','""" + str(_Duration) + """', '""" + str(fetchGid[0]) + """', '""" + _Description + """');"""
            cursor.execute(sql)

            conn.commit()
            res = {'message': "schedule changed successfully."}
            return Response(str(res).replace("'", "\""), status=201, mimetype='application/json')

        except Exception as e :
            print(e)
            return error400Response(str(e))

        finally:
            cursor.close()
            conn.close()

    # 데이터 지우기
    def delete(self):
        try:
            #과연 다른 정보들이 필요한가? Sid만 주면 안되남
            parser = reqparse.RequestParser()
            parser.add_argument('sid', type=str)
            args = parser.parse_args()

            _Sid= args['sid']

            #그룹 추가
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute("""select * from SCHEDULE where Sid = '""" + str(_Sid) + """';""" ) 
            fetchSid = cursor.fetchone()

            if fetchSid:
                sql = """DELETE FROM SCHEDULE where Sid = '""" + str(_Sid) + """';"""
            else :
                res = {'message': "schedule does not exists "}
                return Response(str(res).replace("'", "\""), status=406, mimetype='application/json')
            cursor.execute(sql)
            conn.commit()
            res = {'message': "schedule deleted successfully."}
            return Response(str(res).replace("'", "\""), status=201, mimetype='application/json')

        except Exception as e :
            print(e)
            return error400Response(str(e))

        finally:
            cursor.close()
            conn.close()
        

api.add_resource(USER, '/user')
api.add_resource(GROUP, '/group')
api.add_resource(ALLUSER, '/alluser')
api.add_resource(ALLGROUOP, '/allgroup')
api.add_resource(SCHEDULE, '/schedule')


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


