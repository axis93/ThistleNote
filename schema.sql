DROP TABLE if EXISTS users;
DROP TABLE if EXISTS notes;

CREATE TABLE users(
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	user_name VARCHAR(255),
	user_email VARCHAR(255),
	user_password VARCHAR (200)
);


CREATE TABLE notes(

	ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	title_name VARCHAR(255),
	note_body TEXT,
	user_id, INTEGER,
	FOREIGN KEY (user_id) REFERENCES users(id)
);


INSERT INTO users (id, user_name, user_email, user_password) VALUES (1, 'spukaxis', 'spuk@gmail.com', 'pass');
INSERT INTO notes (id, title_name, note_body, user_id) VALUES (1,'my first note', 'This is my first note to check if that works', 1);
insert into notes (id, title_name, note_body, user_id) values (2, 'my second note', 'This is my second note', 1);
