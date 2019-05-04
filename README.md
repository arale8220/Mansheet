# Mansheet
cs360 in 2019 spring

--Installation
After installation in tutorial, there are some errors at pymysql.connect.

@RuntimeError: cryptography is required for sha256_password or caching_sha2_password
install cryptography with right pip version
pip install cryptography (I used pip3)

@pymysql.err.OperationalError: (1045, "Access denied for user 'root'@'localhost' (using password: YES)")
make user and give password in mysql.
ex)) mysql> grant all privileges on *.* to root@localhost identified by 'password' with grant option;
