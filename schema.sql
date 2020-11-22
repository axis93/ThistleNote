DROP TABLE if EXISTS users;
DROP TABLE if EXISTS notes;

CREATE TABLE users(
	user_name VARCHAR(255),
	user_email VARCHAR(255),
	user_password VARCHAR (200)
);


CREATE TABLE 'notes'(
	
	title_name VARCHAR(255),
	note_body TEXT,
	created TIMESTAMP NOT NULL DEFAULT(strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')),
	updated TIMESTAMP NOT NULL DEFAULT(strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')),
	user_id INTEGER,
	FOREIGN KEY(user_id) REFERENCES users(id)
);
