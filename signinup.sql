USE dbasemlt1;

CREATE TABLE IF NOT EXISTS accounts (
	username varchar(50) NOT NULL,
	email varchar(100) NOT NULL,
	pass varchar(255) NOT NULL
);

INSERT INTO accounts VALUES ('test', 'test@test.com','test');
select * from accounts;