-- file name : test.sql
-- pwd : /project_name/app/schema/test.sql
 
CREATE DATABASE mansheet default CHARACTER SET UTF8;
 
use mansheet;

create user 'admin'@'localhost' identified by 'manshinee';

grant all privileges on mansheet.* to 'admin'@'localhost';
 
CREATE TABLE MUSER(
    Uname		varchar(10) NOT NULL PRIMARY KEY,
    Password	VARCHAR(40) NOT NULL
) CHARSET=utf8;

CREATE TABLE MGROUP(
	Gid				int			NOT NULL PRIMARY KEY AUTO_INCREMENT, 
    Gname			varchar(10) NOT NULL,
    Default_group	CHAR(1)		NOT NULL DEFAULT 'N',
    Owner_uname		varchar(10)	NOT NULL,
    FOREIGN KEY(Owner_uname) REFERENCES MUSER(Uname)
) CHARSET=utf8;

CREATE TABLE PARTICIPATE(
    Uname		varchar(10) NOT NULL PRIMARY KEY,
    Gid         int         NOT NULL,
    FOREIGN KEY(Uname) REFERENCES MUSER(Uname),
    FOREIGN KEY(Gid) REFERENCES MGROUP(Gid)
) CHARSET=utf8;

CREATE TABLE SCHEDULE(
    Start_time	varchar(16) NOT NULL,
    Description	VARCHAR(40),
    Uname 		varchar(10) NOT NULL,
    Gid 		int 		NOT NULL,
    FOREIGN KEY(Uname) REFERENCES MUSER(Uname),
    FOREIGN KEY(Gid) REFERENCES MGROUP(Gid)
) CHARSET=utf8;





