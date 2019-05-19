# Mansheet
cs360 in 2019 spring


# 서버 실행
## make database 
mysql 연결 후 sorce app/schema/makeMansheet.sql 실행

## 서버 API 실행
python3 newvenv/api.py. ~~run file 아님~~

## Installation
실행 시에 아래 에러들 뜨면 추가로 설치해주기

@RuntimeError: cryptography is required for sha256_password or caching_sha2_password
pip install cryptography ~~나는 pip3로 받아서 아래부터는 다 pip3로 쓸게요~~

@(1044, "Access denied for user 'admin'@'%' to database 'mansheet'")
-계정 추가 및 prviileges 설정 후 flush 반드시 해야!
-root에서 create roll 하고 롤에 설정한 privilege를 적용하면 에러가 나는 것 같다.
  그냥 계정 자체에 privilege 추가해주면 오류가 안생긴다. ~~이럴거면 왜 롤을 만든거지~~
-grant로 새로운 유저 만들면 에러. create로 만들고 나서 grant로 privilege 옵션으로 주기
-우선은 admin@manshinee로 설정. 

@ModuleNotFoundError: No mpodule named 'flask_restful'
pip3 install flask-restful

@ModuleNotFoundError: No mpodule named 'flask'
pip3 install flask



# API : JSON in Body
우선 127.0.0.1:5000 기준
## /user [POST] 
```json
{
	"username" : "아이디",
	"password" : "비밀번호"
}
```
### Ressponse status 406 with "Message"
username의 제일 앞 두 글자가 정수가 아닌 경우
제일 앞의 두 글자와 뒤의 단어 사이에 띄어쓰기가 존재하는 경우
아이디가 10글자를 넘어가는 경우
비밀번호가 4자보다 짧은 경우
비밀번호가 40자보다 긴 경우
이미 존재하는 아이디인 경우
### Response status 201 with "Message"
성공적으로 아이디를 생성한 경우

## /user [DELETE] 
```json
{
	"username" : "아이디",
	"password" : "비밀번호"
}
```
### Ressponse status 406 with "Message"
존재하지 않는 아이디를 전달한 경우
옳지 않은 비밀번호를 입력한 경우
### Ressponse status 200 with "Message"
성공적으로 아이디를 제거한 경우













