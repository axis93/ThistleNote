from thistleapp import db

class User(db.Model):
    __tablename__ = 'users'
    


    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String())
    user_email = db.Column(db.String())
    user_password = db.Column(db.String())

    def __init__(self, username, user_email, user_password):
        self.username
        self.user_email
        self.user_password

    def __repr__(self):
        return '<id {}>'.format(self.id)

    def serialize(self):
        return {
                'id': self.id,
                'username': self.username,
                'user_email': self.user_name,
                'user_password': self.user_password
             }



class Note(db.Model):
    __tablename__ = 'notes'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title_name = db.Column(db.String(), nullable=False)
    note_body = db.Column(db.String())
    created = db.Column(db.DateTime) 
    updated = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title_name, note_body, created, updated, user_id):
        self.title_name
        self.note_body
        self.created
        self.updated
        self.user_id
        
    def serialize(self):
        return{
                'id': self.id,
                'title_name': self.title_name,
                'note_body': self.note_body,
                'created': self.created,
                'updated': self.updated,
                'user_id': self.user_id
            }
