from flask import Flask, render_template, redirect, url_for, request, session, flash, g, send_from_directory
from flask_bootstrap import Bootstrap
from flask_datepicker import datepicker
from werkzeug import secure_filename
from datetime import datetime
import sqlite3
import os
from forms import ContactForm, PageDown
from flask_mail import Message, Mail
from flask_pagedown import PageDown

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

@app.route('/')
def home():
    db = get_db() 
    notes = db.cursor().execute('SELECT * FROM notes').fetchall()
    db.close()
    
    return render_template('home.html', allnotes = notes, isHome=True)



@app.route('/markdown', methods = ['GET', 'POST'])
def markdown():
    form = PageDownFormExample()
    text = None
    if form.validate():
       text = form.pageDown.data
    else:
        form.pageDown.data = ('Please enter here your note\n')
       # do something interesting with the Markdown text
    return render_template('markdown.html', form = form, text = text)


@app.route('/contactus', methods=['GET', 'POST'])
def contact():
    form = ContactForm()

    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required. Please fill in the form.')
            return render_template('contactus.html', form=form)
        else:
            msg = Message(form.subject.data, sender=form.email.data, recipients=['simone.piazzini@gmail.com'])
            msn.body= """
            From: %s &lt;%s&gt;
            %s
            """ % (form.name.data, form.email.data, form.message.data)
            mail.send(msg)

            return render_template('contactus.html', success=True)
        
    elif request.method == 'GET':
        return render_template('contactus.html', form = form)

@app.route('/help/')
def help():
    return render_template('help.html')

@app.route('/about')
def about():
   # db = get_db()
   # db.cursor().execute('insert into notes (title_name,  
    return render_template('about.html')

@app.route('/note/', methods=['POST','GET', 'PUT', 'DELETE'])
def note():
    db = get_db()
    if request.method == 'POST':
        new_title_name = request.form.get("title")
        created = datetime.now()
        updated = datetime.now()
        note_body = request.form.get("body")
        user_id = session['id']
        db.cursor().execute('insert into notes (title_name, note_body, user_id) VALUES (?,?, ?)', (new_title_name, note_body, user_id))

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

    if request.method == 'DELETE':
        db.cursor().execute('DELETE from notes where id=?', [id])
        db.commit()
        return redirect(url_for('dashboard.html', username=sesssion['username']))
    return render_template('notes.html')


@app.route('/<username>/dashboard/', methods=['GET', 'POST'])
def dashboard(username):
    db = get_db()
       
      # db.commit()
        
        # I would like to store the file permanently on the server too
    if request.method == 'GET':
        notes = db.cursor().execute('SELECT * FROM notes').fetchall()
        
        return render_template('dashboard.html', allnotes=notes)
   # return render_template('dashboard.html', allnotes=allnotes)

@app.route('/login', methods=['GET',   'POST'])
def login():
    if request.method == 'POST':
        db = get_db()
        username = request.form.get("username")
        email = request.form.get("email")
        
        user = db.cursor().execute('select * from users where user_name = ?', [username])
        if user is None:
            msg = "No user found, please try again"
        else:
            session['username'] = request.form['username']
            
        return redirect(url_for('dashboard', username=request.form['username']))
       # else:
        #    flash('Wrong credentials inserted. Please try again')
         #   return render_template('login.html')
    else:
        if session != None:
            msg = "We are sorry but you are logged in already, I am afraid you will not be able to login until you first logout"

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session['username'] = None 
    return render_template('home.html')

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        db = get_db()

        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        if not email or not password:
            return "You have missed something, please try again"
        new_dir = os.path.join(app.config['ACCOUNT_FOLDERS'], username)
        os.mkdir(new_dir)
        db.cursor().execute('insert into users (user_name, user_email, user_password) VALUES (?,?,?)', (username, email, password) )
        db.commit()
        msg = "You have created the user: " + username
        return render_template('login.html', msg = msg)
        
    return render_template('signup.html')


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
        page='''
        <html>
        <body>
        <form action="" method="post" name="form" enctype="multipart/form-data">
            <input type="file" name="datafile" />
            <input type="submit" name="submit" id="submit" />
        </form>
        </body>
        </html>
        '''
        return page, 200


@app.route('/uploads/file')
def uploaded_file(filename):
    return send_from_directory('static/uploads/',filename )

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)

