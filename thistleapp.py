from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_bootstrap import Bootstrap

app = Flask(__name__)
Bootstrap(app)
app.secret_key = 'Aksdf304.asd;sajad;2sadadsa;lvna;l~~23cx:s1a>Mdb'

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

@app.route('/spukaxis/dashboard/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/login', methods=['GET',   'POST'])
def login():
    if request.method == 'POST':
        if request.form['Password'] == 'porcodio' and request.form['username'] == 'spukaxis':
            
            return redirect(url_for('dashboard'))
        else:
            flash('Wrong credentials inserted. Please try again')
            return render_template('login.html')

    return render_template('login.html')

@app.route('/signup', methods=['GET','POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        if not email or not password:
            return "You have missed something, please try again"
        return render_template('login.html')
    return render_template('signup.html')
@app.route('/upload/', methods=['POST','GET'])
def upload():
    if request.method == 'POST':
        f = request.files['datafile']
        f.save('static/uploads/filename')
        return "File Uploaded"
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


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)


