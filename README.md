# Mansheet
cs360 in 2019 spring


## mysql, flask installation
### mysql
1. https://dev.mysql.com/downloads/mysql/
2. 설치 도중 root user의 password 설정하기
3. 완료 후 터미널에 $ mysql -u root -p (앞에서 설정한 패스워드)

### Flask 설치
1. Python 3.7 ==> https://www.python.org/
2. virtualenv ==> https://virtualenv.pypa.io/en/latest/
3. Flask ==> 터미널에 $ pip3 install Flask
4. PyMySQL ==> $ pip3 install PyMySQL
<br/>
<br/>
<br/>

## 서버 실행
1. make database <br/>
mysql 연결 후 source app/schema/makeMansheet.sql 실행

2. 서버 API 실행<br/>
python3 newvenv/api.py.   ~~run file 아님~~
<br/>
<br/>
<br/>

## Installation
실행 시에 아래 에러들 뜨면 추가로 설치해주기

@RuntimeError: cryptography is required for sha256_password or caching_sha2_password<br/>
pip install cryptography ~~나는 pip3로 받아서 아래부터는 다 pip3로 쓸게요~~

@(1044, "Access denied for user 'admin'@'%' to database 'mansheet'")<br/>
-계정 추가 및 prviileges 설정 후 flush 반드시 해야!<br/>
-root에서 create roll 하고 롤에 설정한 privilege를 적용하면 에러가 나는 것 같다.<br/>
  그냥 계정 자체에 privilege 추가해주면 오류가 안생긴다. ~~이럴거면 왜 롤을 만든거지~~<br/>
-grant로 새로운 유저 만들면 에러. create로 만들고 나서 grant로 privilege 옵션으로 주기<br/>
-우선은 admin@manshinee로 설정. <br/>

@ModuleNotFoundError: No mpodule named 'flask_restful'<br/>
pip3 install flask-restful

@ModuleNotFoundError: No mpodule named 'flaskext'<br/>
pip3 install flask-mysql

@ModuleNotFoundError: No mpodule named 'flask'<br/>
pip3 install flask

@ModuleNotFoundError: No mpodule named 'flask_cors'<br/>
pip3 install flask_cors

<br/>
<br/>
<br/>
<br/>
<br/>

# API : JSON in Body, 127.0.0.1:5000
## 회원가입 /user [POST] 
body json input
```json
====input====
{
	"username" : "아이디",
	"password" : "비밀번호"
}
```
#### Ressponse status 406 with "Message"
username의 제일 앞 두 글자가 정수가 아닌 경우<br/>
제일 앞의 두 글자와 뒤의 단어 사이에 띄어쓰기가 존재하는 경우<br/>
아이디가 10글자를 넘어가는 경우<br/>
아이디가 4자보다 짧은 경우<br/>
비밀번호가 4자보다 짧은 경우<br/>
비밀번호가 40자보다 긴 경우<br/>
이미 존재하는 아이디인 경우<br/>
```json
====output====
{
	"message" : "Message"
}
```
#### Response status 201 with "Message"
성공적으로 아이디를 생성한 경우
```json
====output====
{
	"message" : "Message",
	"username" : "아이디",
	"password" : "비밀번호"
}
```


<br/>
<br/>

## 탈퇴 /user [DELETE] 
```json
====input====
{
	"username" : "아이디",
	"password" : "비밀번호"
}
```
#### Ressponse status 406 with "Message"
존재하지 않는 아이디를 전달한 경우<br/>
옳지 않은 비밀번호를 입력한 경우
```json
====output====
{
	"message" : "Message"
}
```
#### Ressponse status 200 with "Message"
성공적으로 아이디를 제거한 경우
```json
====output====
{
	"message" : "Message"
}
```


<br/>
<br/>


## 로그인 /user [PATCH] 
```json
====input====
{
	"username" : "아이디",
	"password" : "비밀번호"
}
```
#### Ressponse status 406 with "Message"
존재하지 않는 아이디를 전달한 경우<br/>
옳지 않은 비밀번호를 입력한 경우
```json
====output====
{
	"message" : "Message"
}
```
#### Ressponse status 200 with "Message"
성공적으로 로그인된 경우
```json
====output====
{
	"message" : "Message",
	"username" : "아이디",
	"password" : "비밀번호",
	"defaultgid" : 00
}
```

<br/>
<br/>



## 그룹 생성 /group [POST] 
```json
====input====
{
	"username" : "아이디",
	"groupname" : "그룹 이름",
	"entries" : [
		{"username" : "탑을 제외한 엔트리 이름"},
		,,,
	]
}
```
#### Ressponse status 406 with "Message"
그룹 이름의 길이가 1글자보다 짧은 경우<br/>
그룹 이름의 길이가 30글자보다 긴 경우<br/>
이미 같은 이름의 그룹이 존재하는 경우<br/>
```json
====output====
{
	"message" : "Message"
}
```
#### Ressponse status 201 with "Message"
성공적으로 그룹을 만든 경우
```json
====output====
{
	"message" : "Message",
	"ownername" : "아이디",
	"groupname" : "그룹 이름",
	"groupid" : 00,
	"schedules" : [
        {
        	"Sid" : 00,
            "Start_date": "2019-05-20",
            "Start_time": "20:00",
            "Duration" : 60,
            "Description": "안녕",
            "Uname": "00hi",
            "Gid": 1
        },
        ,,, "엔트리와 탑의 모든 일정들, 그룹의 일정들"
    ],
    "entries" : [
    	{
    		"username" : "아이디"
    	},
    	,,, "탑을 제외한 엔트리의 이름"
    ]
}
```

<br/>
<br/>

## 그룹 정보 /group [PATCH] 
```json
====input====
{
	"groupname" : "그룹 이름"
}
```
#### Ressponse status 200
```json
====output====
{
	"ownername" : "아이디",
	"groupname" : "그룹 이름",
	"schedules" : [
        {
        	"sid" : 00
            "start_date": "2019-05-20",
            "start_time": "20:00",
            "duration" : 00,
            "description": "안녕",
            "username": "00hi",
            "groupid": 00,
            "groupname" : "test"
        },
        ,,,
    ],
    "entries" : [
    	{
    		"username" : "아이디"
    	},
    	,,,
    ]
}
```


<br/>
<br/>


## 모든 그룹의 간략한 정보 /allgroup [PATCH] 
```json
====input====
{
	"username" : "유저 이름"
}
```
#### Ressponse status 200

유저가 속해있지 않고, 디폴트 그룹(개인 일정)이 아닌 그룹들만 반환

```json
====output====
[
	{
		"ownername" : "아이디",
		"groupname" : "그룹 이름",
		"groupid" : "그룹 아이디",
	    "entries" : [
	    	{
	    		"username" : "탑을 제외한 엔트리의 아이디"
	    	},
	    	,,,
	    ]
	},
	,,,
]
```


<br/>
<br/>


## 모든 유저의 간략한 정보 /alluser [PATCH] 
```json
====input====
{
	"username" : "유저 이름"
}
```
#### Ressponse status 200
```json
====output====
[
	{
		"username" : "인풋으로 준 유저를 제외한 모든 유저"
	},
	,,,
]
```

<br/>
<br/>


## 스케쥴 정보 /schedule [POST]
```json
====input====
{
    "groupname": "Group Name",
    "username": "User Name",
    "start_date": "0000-00-00",
    "start_time": "00:00",
    "duration": 60,
    "description": "description this can be none"
}
```
#### Ressponse status 200
성공적으로 스케쥴이 등록된 경우
```json
====output====
{
    "message": "Message"
}
```


<br/>
<br/>


## 스케쥴 정보 /schedule [Patch]
```json
====input====
{
    "sid" : "target schedule sid which will be deleted",
    # below this is used to change schedule
    "start_date" : "start_date",
    "start_time" : "start_time",
    "username" : "username",
    "groupname" : "groupname",
    "description" : "description",
    "duration" : ""
}
```
#### Ressponse status 200
성공적으로 스케쥴이 변경된 경우
```json
====output====
{
    "message": "Message"
}
```


<br/>
<br/>



## 스케쥴 정보 /schedule [DELETE]
```json
====input====
{
    "sid":"sid"
}
```
#### Ressponse status 200
성공적으로 스케쥴이 삭제된 경우
```json
====output====
{
    "message": "Message"
}
```












<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>
<br/>










## 하는중인거


## 그룹 정보 /group [DELETE] 
```json
====input====
{
	"groupname" : "그룹 이름",
	"username" : "현재 로그인된 유저 이름"
}
```
#### Ressponse status 200
```json
====output====
{
	"message" : "Message"
}
```



