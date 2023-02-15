drop database if exists library;

create database library;

drop database if exists test_library;
create database test_library;

use mysql;
create user 'api'@'%' identified by '1234pass';
grant all privileges on library.* to 'api'@'%';
GRANT all privileges on test_library.* to 'api'@'%';