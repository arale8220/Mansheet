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


## 서버 실행
1. make database <br/>
mysql 연결 후 source app/schema/makeMansheet.sql 실행

2. 서버 API 실행<br/>
python3 newvenv/api.py.   ~~run file 아님~~

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




## 로그인 /user [GET] 
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
	"schedules" : [
        {
            "Start_date": "2019-05-20",
            "Start_time": "20:00",
            "Description": "안녕",
            "Uname": "00hi",
            "Gid": 1
        },
        ,,,
    ]
}
```














