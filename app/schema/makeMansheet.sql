-- file name : test.sql
-- pwd : /project_name/app/schema/test.sql

DROP DATABASE mansheet;
CREATE DATABASE mansheet default CHARACTER SET UTF8;
USE mansheet;

drop user 'admin'@'localhost';
create user 'admin'@'localhost' identified by 'manshinee';
grant all privileges on mansheet.* to 'admin'@'localhost';
 
CREATE TABLE MUSER(
    Uname		varchar(10) NOT NULL PRIMARY KEY,
    Password	VARCHAR(40) NOT NULL
) CHARSET=utf8;

CREATE TABLE MGROUP(
	Gid				int			NOT NULL PRIMARY KEY AUTO_INCREMENT, 
    Gname			varchar(30) NOT NULL,
    Default_group	CHAR(1)		NOT NULL DEFAULT 'N',
    Owner_uname		varchar(10)	NOT NULL,
    FOREIGN KEY(Owner_uname) REFERENCES MUSER(Uname)
) CHARSET=utf8;

CREATE TABLE PARTICIPATE(
    Uname		varchar(10) NOT NULL,
    Gid         int         NOT NULL,
    FOREIGN KEY(Uname) REFERENCES MUSER(Uname),
    FOREIGN KEY(Gid) REFERENCES MGROUP(Gid)
) CHARSET=utf8;

CREATE TABLE SCHEDULE(
    Start_date  varchar(10) NOT Null,
    Start_time	varchar(15) NOT NULL,
    Description	VARCHAR(40),
    Uname 		varchar(10) NOT NULL,
    Gid 		int 		NOT NULL,
    FOREIGN KEY(Uname) REFERENCES MUSER(Uname),
    FOREIGN KEY(Gid) REFERENCES MGROUP(Gid)
) CHARSET=utf8;


DELIMITER $$

DROP PROCEDURE IF EXISTS createMuser $$ 
CREATE PROCEDURE createMuser(
    IN  _Uname      VARCHAR(10), 
    IN  _Password   VARCHAR(40),
    OUT RESULT      INT
)
BEGIN
    DECLARE exit handler for SQLEXCEPTION
    BEGIN
        ROLLBACK;        
        SET RESULT = 0;  
    END;
    INSERT INTO MUSER VALUES (_Uname, _Password);
    START TRANSACTION;
        INSERT INTO MGROUP (Gname, Default_group, Owner_uname) VALUES (_Uname, 'Y', _Uname);
        INSERT INTO PARTICIPATE VALUES (_Uname, last_insert_id() );
    COMMIT;
    SET RESULT = 1;
END $$



DROP PROCEDURE IF EXISTS deleteMuser $$ 
CREATE PROCEDURE deleteMuser(
    IN  _Uname      VARCHAR(10), 
    IN  _Password   VARCHAR(40),
    OUT RESULT      INT
)
BEGIN
    DECLARE exit handler for SQLEXCEPTION
    BEGIN
        ROLLBACK;        
        SET RESULT = 0;  
    END;
    START TRANSACTION;
        DELETE FROM SCHEDULE WHERE Uname=_Uname;
        DELETE FROM PARTICIPATE WHERE Uname=_Uname;
        DELETE FROM MGROUP WHERE Owner_uname=_Uname;
        DELETE FROM MUSER WHERE Uname=_Uname;
    COMMIT;
    SET RESULT = 1;
END $$

DELIMITER ;




