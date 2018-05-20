CREATE DATABASE gradesystem;

use gradesystem;

CREATE TABLE student
(
  sid   CHAR(20) NOT NULL,
  sname INT(10) DEFAULT '10',
  gender CHAR(5)
 );

CREATE TABLE course
(
  cid      INT(10),
  cname    CHAR(20)
 );
 
CREATE TABLE mark
(
  mid   INT(10) NOT NULL, 
  sid   INT(10) NOT NULL,
  cid   INT(10), 
  score   INT(10)
 
);
