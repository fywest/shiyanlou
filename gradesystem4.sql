CREATE DATABASE gradesystem;

use gradesystem;

CREATE TABLE student
(
  sid   INT(10) AUTO_INCREMENT PRIMARY KEY,
  sname CHAR(20),
  gender CHAR(10)
 );

CREATE TABLE course
(
  cid      INT(10) AUTO_INCREMENT PRIMARY KEY,
  cname    CHAR(20)
 );
 
CREATE TABLE mark
(
  mid   INT(10) AUTO_INCREMENT PRIMARY KEY, 
  sid   INT(10),
  cid   INT(10), 
  score   INT(10) DEFAULT '0',
  CONSTRAINT mark_fk1 FOREIGN KEY (sid) REFERENCES student(sid),
  CONSTRAINT mark_fk2 FOREIGN KEY (cid) REFERENCES course(cid)
);
