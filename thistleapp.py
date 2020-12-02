from flask import Flask, render_template, redirect, url_for, request, session, flash, g, send_from_directory
from flask_bootstrap import Bootstrap
from flask_datepicker import datepicker
#from werkzeug import secure_filename
from datetime import datetime
import sqlite3
import os
from forms import ContactForm, PageDown
from flask_mail import Message, Mail
from wtforms import Form
from flask_pagedown import PageDown
from flask_pagedown.fields import PageDownField
import json
import os.path
from os import path
app = Flask(__name__)


pagedown = PageDown(app)
Bootstrap(app)
datepicker(app)
app.secret_key = 'Aksdf304.asd;sajad;2sadadsa;lvna;l~~23cx:s1a>Mdb'
# next lines have been added for postgresql
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/thistleapp'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db_location = 'var/mydatabase.db'
ALLOWED_EXTENSION = {'txt', 'pdf', 'pptx'}
app.config['ACCOUNT_FOLDERS']='static/users/'
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
# configuration for the email server
app.config['MAIL_SERVER'] = "smtp.gmail.com"
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'sim.pia.work@gmail.com'
app.config['MAIL_PASSWORD'] = 'thisismynewpasswordthatistemporary'
SESSION_TYPE = None

mail = Mail(app)

def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = sqlite3.connect(db_location)
        g.db = db
    return db


@app.teardown_appcontext
def close_db_connection(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

@app.route('/markdown/', methods=['GET', 'POST'])
def some():
    if request.method == 'POST':
        return redirect(url_for('home'))
     #   title = request.form.get(['name'])
      #  body = request.form.get(['body'])
       # file = os.save(app.config['ACCOUNT_FOLDERS'], session['username'], tile, '.md')
        #with open(file, "w") as f:
         #   f.write(body)
        #return render_template('some.html')

    return render_template('markdown.html')

@app.route('/')
def home():
    db = get_db() 
    notes = db.cursor().execute('SELECT * FROM notes').fetchall()
    db.close()
    
    return render_template('home.html', allnotes = notes, isHome=True)



@app.route('/markdown', methods = ['GET', 'POST'])
def markdown():
    form = PageDown()
    text = None
    
    text = form.pageDown
       # do something interesting with the Markdown text
    return render_template('markdown.html', form = form, text = text)


@app.route('/contactus', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    msg = ""
    if request.method == 'POST':
        if form.validate() == False:
            msg = 'All fields are required. Please fill in the form.'
            return render_template('contactus.html', form=form)
        else:
            name = request.form['name']
            email = request.form['email']
            subject = request.form['subject']
            message = request.form['message']
            with open('static/messages/messages.json', 'a') as f:
                json.dump(request.form, f)
            msg = "Thanks we received your email"
            return render_template('contactus.html', msg = msg, success=True)
        
    elif request.method == 'GET':
        return render_template('contactus.html', form = form, msg = msg)

@app.route('/help/')
def help():
    return render_template('help.html')

@app.route('/about')
def about():
   # db = get_db()
   # db.cursor().execute('insert into notes (title_name,  
    return render_template('about.html')




@app.route('/note/', methods=['POST','GET'])
def note():
    db = get_db()
    if request.method == 'POST':
        new_title_name = request.form.get("title")
        created = datetime.now()
        updated = datetime.now()
        note_body = request.form.get("body")
        user_id = session['id']
        db.cursor().execute('insert into notes (title_name, note_body, user_id) VALUES (?,?,?)', (new_title_name, note_body, user_id))

        db.commit()
        return redirect(url_for('dashboard', username=session['username']))
    
    # I would like to store the file permanently on the server too
   # db = get_db()
   # note = None
   # if request.method == 'GET':

    #    db.cursor().execute('SELECT * from notes WHERE title_name=?', ['title'])
     #   rows = db.cursor().fetchall()
      #  for r in rows:
       #     note = r
       # if note is not None:
        #    return "well done"
       # else:
        #    return "Something went wrong", 404
   # if request.method == 'POST':
    #    return "you did it!"

   # if request.method == 'PUT':
    #    title_name = request.form["title"]
     #   updated = datetime.now()
        # INCOMPLETE/INCORRECT SQL STATEMENT
      #  db.cursor().execute('UPDATE note SET title_name=?, update=? WHERE id=?', [id])        
       # db.commit()
        #return "The note has been updated", 200
    return render_template('notes.html')
@app.route('/note/edit/<id>', methods=['GET', 'POST'])
def edit():
    db = get_db

@app.route('/<username>/dashboard/', methods=['GET', 'POST'])
def dashboard(username):
    db = get_db()
       
      # db.commit()
        
        # I would like to store the file permanently on the server too
    if request.method == 'GET':
        user = db.cursor().execute('SELECT * from users where user_name = ?', [username]).fetchone()
        id = user[0]
        session['id'] = id
        notes = db.cursor().execute('SELECT * FROM notes WHERE user_id = ?', [id]).fetchall()

        return render_template('dashboard.html', allnotes=notes)
   # return render_template('dashboard.html', allnotes=allnotes)

@app.route('/login', methods=['GET',   'POST'])
def login():
    if request.method == 'POST':
        db = get_db()
        username = request.form.get("username")
        password = request.form.get("password")
        if not username or not password:
            msg = "Please enter email and passowrd"
        cur = db.cursor()
        cur.execute('SELECT * from users where user_name = ?', [username])
        user = cur.fetchone()
        if user is None:
            msg = "No user found, please try again"
        else:
            session['username'] = username
            session['id'] = user[0]

            return redirect(url_for('dashboard', username=request.form['username']))
       # else:
        #    flash('Wrong credentials inserted. Please try again')
         #   return render_template('login.html')
    else:
        
            msg = "Please enter your details to login. You username should be enough"

    return render_template('login.html', msg = msg)

@app.route('/logout')
def logout():
    session.pop('username', None)
    session['username'] = None 
    return render_template('home.html'), 200

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        db = get_db()

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        if not email or not password or not username:
            msg = "Please enter all the fields"
            return render_template('signup.html', msg = msg)
        cur = db.cursor()
        cur.execute('SELECT * from users where user_name = ?', [username])
        user = cur.fetchone()
        if user is not None:
            msg = "User exists, please try again"
            return render_template('signup.html', msg = msg)
    
        db.cursor().execute('insert into users (user_name, user_email, user_password) VALUES (?,?,?)', (username, email, password) )
        db.commit()
        new_dir = os.path.join(app.config['ACCOUNT_FOLDERS'], username)
        os.mkdir(new_dir)
        msg = "You have created the user: " + username
        return render_template('login.html', msg = msg)
        
    msg = "Please enter your new credentials"
    return render_template('signup.html', msg = msg), 200


def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSION

@app.route('/upload/', methods=['POST','GET'])
def upload():
    if request.method == 'POST':
        f = request.files['datafile']    
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], f.filename))
        f = f.filename
        flash('You have successfully uploaded a file')
        return send_from_directory('static/uploads/', f )
    else:

        return render_template("upload.html"), 200


@app.route('/uploads/file')
def uploaded_file(filename):
    return send_from_directory('static/uploads/',filename )

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

