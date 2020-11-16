CREATE TABLE 'users'(
	'id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	'user_name' VARCHAR(255),
	'user_email', VARCHAR(255),
	'user_password', VARCHAR (200)
);


CREATE TABLE 'notes'(
	
	'note_id' INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	'title_name' VARCHAR(255),
	'note_body' TEXT,
	'created' TIMESTAMP NOT NULL DEFAULT(strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')),
	'updated' TIMESTAMP NOT NULL DEFAULT(strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')),
	'user_id' INTEGER,
	FOREIGN KEY(user_id) REFERENCES users(id)
);
