DROP TABLE if EXISTS users;
DROP TABLE if EXISTS notes;

CREATE TABLE users(
	id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	user_name VARCHAR(255),
	user_email VARCHAR(255),
	user_password VARCHAR (200)
);


CREATE TABLE notes(

	title_name VARCHAR(255),
	note_body TEXT,
	user_id, INTEGER,
	FOREIGN KEY (user_id) REFERENCES users(id)
);



INSERT INTO notes (title_name, note_body) VALUES ('my first note', 'This is my first note to check if that works');
insert into notes (title_name, note_body) values ('my second note', 'This is my second note');
