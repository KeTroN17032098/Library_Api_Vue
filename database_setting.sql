drop database if exists library;

create database library;

use mysql;
create user 'api'@'%' identified by '1234pass';
grant all privileges on library.* to 'api'@'%';