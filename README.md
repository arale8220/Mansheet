# Mansheet
cs360 in 2019 spring

## Installation
After installation in tutorial, there are some errors at pymysql.connect.

### @RuntimeError: cryptography is required for sha256_password or caching_sha2_password
install cryptography with right pip version
pip install cryptography ~~근데 우린 python 3 쓸거라 pip3로 쓰는 습관 가지쟈~~

### @(1045, "Access denied for user 'root'@'localhost' (using password: YES)")
튜토리얼 파일 실행할거면 파일 내 root의 비밀번호 설정

### @(1044, "Access denied for user 'admin'@'%' to database 'mansheet'")
-계정 추가 및 prviileges 설정 후 flush 반드시 해야!
-root에서 create roll 하고 롤에 설정한 privilege를 적용하면 에러가 나는 것 같다.
  그냥 계정 자체에 privilege 추가해주면 오류가 안생긴다. ~~이럴거면 왜 롤을 만든거지~~
-grant로 새로운 유저 만들면 에러. create로 만들고 나서 grant로 privilege 옵션으로 주기
-우선은 admin@manshinee로 개발ing


## 개발 디렉토리 설정
[Project Name : Mansheet]
└ [app]
      └ [static]
            └ 자바스크립트, CSS, 이미지 등...
      └ [templates]
            └ HTML 파일들(폴더별로 정리 가능)
└ run.py

## ubuntu에 python3, pip3 설치
$ sudo apt-get update
$ sudo apt-get dist-upgrade
$ sudo apt-get autoremove
$ sudo apt-get install python3
$ sudo apt-get install python3-pip
$ sudo pip3 install --upgrade pip

