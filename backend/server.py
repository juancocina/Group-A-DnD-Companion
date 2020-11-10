import flask
from flask import *
import sqlite3, hashlib, os, requests
from flask import request, url_for, redirect
from werkzeug.utils import secure_filename
from flask_login import LoginManager
#from config import Config

app = flask.Flask(__name__)
app.config.from_envvar('APP_CONFIG')

login = LoginManager()

def getLoginDetails():
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        if 'email' not in session:
            loggedIn = False
            firstName = ''
            noOfItems = 0
        else:
            loggedIn = True
            cur.execute("SELECT userId, firstName FROM users WHERE email = '" + session['email'] + "'")
            userId, firstName = cur.fetchone()
            cur.execute("SELECT count(productId) FROM kart WHERE userId = " + str(userId))
            noOfItems = cur.fetchone()[0]
    conn.close()
    return (loggedIn, firstName, noOfItems)

@app.route("/")
def root():
    return redirect(url_for('welcome'))

@app.route("/welcome")
def welcome():
    return render_template('welcome.html')

@app.route("/login")
def test_login():
    return render_template('test_login_page.html')

@app.route('/on_register', methods=['POST'])
def test_register():
    if request.method == 'POST':
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]
        return render_template("test_login_page.html")

@app.route('/register')
def test_register_form():
    return render_template("register.html")


@app.route("/account/profile")
def profileHome():
    if 'email' not in session:
        return redirect(url_for('root'))
    loggedIn, firstName, noOfItems = getLoginDetails()
    return render_template("profileHome.html", loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems)

@app.route("/account/profile/edit")
def editProfile():
    if 'email' not in session:
        return redirect(url_for('root'))
    loggedIn, firstName, noOfItems = getLoginDetails()
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT userId, email, firstName, lastName, address1, address2, zipcode, city, state, country, phone FROM users WHERE email = '" + session['email'] + "'")
        profileData = cur.fetchone()
    conn.close()
    return render_template("editProfile.html", profileData=profileData, loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems)

@app.route("/account/profile/changePassword", methods=["GET", "POST"])
def changePassword():
    if 'email' not in session:
        return redirect(url_for('loginForm'))
    if request.method == "POST":
        oldPassword = request.form['oldpassword']
        oldPassword = hashlib.md5(oldPassword.encode()).hexdigest()
        newPassword = request.form['newpassword']
        newPassword = hashlib.md5(newPassword.encode()).hexdigest()
        with sqlite3.connect('database.db') as conn:
            cur = conn.cursor()
            cur.execute("SELECT userId, password FROM users WHERE email = '" + session['email'] + "'")
            userId, password = cur.fetchone()
            if (password == oldPassword):
                try:
                    cur.execute("UPDATE users SET password = ? WHERE userId = ?", (newPassword, userId))
                    conn.commit()
                    msg="Changed successfully"
                except:
                    conn.rollback()
                    msg = "Failed"
                return render_template("changePassword.html", msg=msg)
            else:
                msg = "Wrong password"
        conn.close()
        return render_template("changePassword.html", msg=msg)
    else:
        return render_template("changePassword.html")

@app.route("/updateProfile", methods=["GET", "POST"])
def updateProfile():
    if request.method == 'POST':
        email = request.form['email']
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        address1 = request.form['address1']
        address2 = request.form['address2']
        zipcode = request.form['zipcode']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        phone = request.form['phone']
        with sqlite3.connect('database.db') as con:
                try:
                    cur = con.cursor()
                    cur.execute('UPDATE users SET firstName = ?, lastName = ?, address1 = ?, address2 = ?, zipcode = ?, city = ?, state = ?, country = ?, phone = ? WHERE email = ?', (firstName, lastName, address1, address2, zipcode, city, state, country, phone, email))

                    con.commit()
                    msg = "Saved Successfully"
                except:
                    con.rollback()
                    msg = "Error occured"
        con.close()
        return redirect(url_for('editProfile'))

# @app.route("/loginForm")
# def loginForm():
#     if 'email' in session:
#         return redirect(url_for('root'))
#     else:
#         return render_template('login.html', error='')

# @app.route("/login", methods = ['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('test'))
#     form = Loginform()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.username.data).first()
#         if user is None or not user.check_password(form.password.data):
#             flash('Invalid username or password')
#             return redirect(url_for('login'))
#         login_user(user, remember=form.remember_me.data)
#         return redirect(url_for('test'))
#     return render_template('login.html', title='Sign In', form=form)


@app.route("/logout")
def logout():
    session.pop('email', None)
    return redirect(url_for('root'))

def is_valid(email, password):
    con = sqlite3.connect('database.db')
    cur = con.cursor()
    cur.execute('SELECT email, password FROM users')
    data = cur.fetchall()
    for row in data:
        if row[0] == email and row[1] == hashlib.md5(password.encode()).hexdigest():
            return True
    return False


# @app.route("/register", methods = ['GET', 'POST'])
# def register():
#     if request.method == 'POST':
#         #Parse form data
#         password = request.form['password']
#         email = request.form['email']
#         firstName = request.form['firstName']
#         lastName = request.form['lastName']
#         address1 = request.form['address1']
#         address2 = request.form['address2']
#         zipcode = request.form['zipcode']
#         city = request.form['city']
#         state = request.form['state']
#         country = request.form['country']
#         phone = request.form['phone']

#         with sqlite3.connect('database.db') as con:
#             try:
#                 cur = con.cursor()
#                 cur.execute('INSERT INTO users (password, email, firstName, lastName, address1, address2, zipcode, city, state, country, phone) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', (hashlib.md5(password.encode()).hexdigest(), email, firstName, lastName, address1, address2, zipcode, city, state, country, phone))

#                 con.commit()

#                 msg = "Registered Successfully"
#             except:
#                 con.rollback()
#                 msg = "Error occured"
#         con.close()
#         return render_template("login.html", error=msg)



# @app.route("/registerationForm")
# def registrationForm():
#     return render_template("register.html")

# testing page communication ---- Juan
@app.route("/faq")
def faq():
    return render_template("faq.html")

@app.route("/howtoplay")
def howtoplay():
    return render_template("howtoplay.html")

# End of testing page communication...

def allowed_file(filename):
    return '.' in filename and \
            filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

def parse(data):
    ans = []
    i = 0
    while i < len(data):
        curr = []
        for j in range(7):
            if i >= len(data):
                break
            curr.append(data[i])
            i += 1
        ans.append(curr)
    return ans

if __name__ == '__main__':
    app.run()
