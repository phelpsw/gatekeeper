use gatekeeper;

DROP TABLE gates;
DROP TABLE users;
DROP TABLE log;

CREATE TABLE users (
	id INT NOT NULL AUTO_INCREMENT,
	name VARCHAR(100) NOT NULL,
	creation_time DATETIME NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE gates (
	id INT NOT NULL AUTO_INCREMENT,
	user_id INT NOT NULL,
	source VARCHAR(20) NOT NULL,
	extension INT NOT NULL,
	state ENUM('allow', 'deny', 'forward') NOT NULL,
	access_message VARCHAR(100),
	access_code VARCHAR(100) NOT NULL,
	denial_message VARCHAR(100),
	forward_number VARCHAR(20),
	creation_time DATETIME NOT NULL,
	PRIMARY KEY(id)
);

CREATE TABLE log (
	id INT NOT NULL AUTO_INCREMENT,
	sid VARCHAR(100) NOT NULL,
	action VARCHAR(40) NOT NULL,
	extension INT,
	time DATETIME NOT NULL,
	PRIMARY KEY(id)
);

INSERT INTO users (name, creation_time) VALUES ('Phelps', NOW());
INSERT INTO gates (user_id,
		   source,
		   extension,
		   state,
		   access_message,
		   access_code,
		   denial_message,
		   forward_number,
		   creation_time) VALUES
('1', '15553755828', '1000', 'allow', 'Access granted.', '9', 'Entry denied.', '15553755828', NOW());
