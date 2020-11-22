from flask import Flask, render_template, redirect, url_for, request, session, flash, g, send_from_directory
from flask_bootstrap import Bootstrap
from flask_datepicker import datepicker
from werkzeug import secure_filename
import sqlite3
import os


app = Flask(__name__)

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

    return render_template('home.html',)

@app.route('/contactus/')
def contact():
    return render_template('contactus.html')

@app.route('/help/')
def help():
    return render_template('help.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/note')
def note():
    return render_template('notes.html')

@app.route('/<username>/dashboard/')
def dashboard(username):
    return render_template('dashboard.html')

@app.route('/login', methods=['GET',   'POST'])
def login():
    if request.method == 'POST':
        if request.form['Password'] == 'porcodio' and request.form['username'] == 'spukaxis':
            
            
            return redirect(url_for('dashboard', username=request.form['username']))
        else:
            flash('Wrong credentials inserted. Please try again')
            return render_template('login.html')

    return render_template('login.html')

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
        flash('You have successfully uploaded a file')
        return uploaded_file(f)
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


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    f = request.files['datafile']
    return send_from_directory('static/uploads/', filename)


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)


