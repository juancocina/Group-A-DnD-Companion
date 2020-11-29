import flask
from flask import *
import sqlite3, hashlib, os, requests
from flask import request, url_for, redirect, flash
from werkzeug.utils import secure_filename
from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from aux_functions.CharacterCreator_v1_3 import *
from aux_functions.account_queries import *
from aux_functions.campaign_creator import *
# from aux_functions.UpdateCharacter import *
#from config import Config

app = flask.Flask(__name__)
app.config.from_envvar('APP_CONFIG')
app.secret_key = app.config['SECRET_KEY']

registration_required = app.config['REGISTER_USER_REQUIRED']

login = LoginManager()

DATABASE_USERS = app.config['DATABASE_USERS']
DATABASE_CHARACTER = app.config['DATABASE_CHARACTER']

#################################
# Database Handling Definitions #
#################################

def get_db(database):
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(database)
    return db




############################
# BACKEND HELPER FUNCTIONS #
############################


def getLoginDetails():
    with sqlite3.connect(DATABASE_USERS) as conn:
        cur = conn.cursor()
        if 'email' not in session:
            loggedIn = False
            username = ''
        else:
            loggedIn = True
            cur.execute("SELECT user_id, username FROM users WHERE email = ?", (session['email'],))
            user_id, username = cur.fetchone()
    conn.close()
    return (loggedIn, user_id, username)

# Determine if supplied password 
def is_valid(email, password):
    database = get_db(DATABASE_USERS)
    c = database.cursor()
    c.execute("SELECT EXISTS(SELECT hashed_password FROM users WHERE email=?)", (email,))
    data = c.fetchall()[0][0]
    if c.fetchall() == 0:
        return False
    c.execute("SELECT hashed_password FROM users WHERE email=?", ([email]))
    data = c.fetchall()[0][0]
    if check_password_hash(data, password):
        return True
    else:
        return False





#######################
# ROUTING DEFINITIONS #
#######################

@app.route("/")
def root():
    return redirect(url_for('welcome'))

@app.route("/welcome")
def welcome():
    return render_template('welcome.html')

@app.route("/on_login", methods=['POST'])
def on_login():
    if request.method == 'POST':
        email = request.form["email"]
        password = request.form["password"]
        if is_valid(email, password):
            session['email'] = email
            return redirect(url_for('account'))
        else:
            error = 'Invalid email/password'
            return render_template('login.html', error=error)
            
@app.route("/login")
def login():
    if 'email' in session:
        return redirect(url_for('account'))
    else:
        return render_template('login.html')

@app.route('/on_register', methods=['POST'])
def register():
    if request.method == 'POST':
        app.logger.info(f"")
        email = request.form["email"]
        username = request.form["username"]
        password = request.form["password"]
        hashed = generate_password_hash(password, "sha512")

        database = get_db(DATABASE_USERS)
        c = database.cursor()
        c.execute("SELECT EXISTS(SELECT username FROM users WHERE username=? LIMIT 1)", (username,))

        if c.fetchall()[0][0] > 0:
            flash('Username already taken.')
            return flask.flash('Username already taken.')
        
        c.execute("SELECT EXISTS(SELECT email FROM users WHERE email=? LIMIT 1)", (email,))
        if c.fetchall()[0][0] > 0:
            return flask.flash('Email already exists.')

        c.execute("INSERT INTO users (email, username, hashed_password) VALUES (?,?,?)", (email, username, hashed))
        database.commit()
        c.close()
        database.close()
        return render_template("login.html")

@app.route('/register')
def register_form():
    if 'email' not in session:
        return render_template("register.html")
    else:
        return redirect(url_for('account'))

@app.route('/account')
def account():
    if 'email' not in session:
        return redirect(url_for('login'))
    loggedIn, user_id, username = getLoginDetails()
    email = session['email']
    characters = query_account_characters(user_id)
    campaigns = query_account_campaigns(user_id)
    return render_template("fake.html", username=username, email=email, characters=characters, campaigns=campaigns)


@app.route("/account/profile")
def profileHome():
    if 'email' not in session:
        return redirect(url_for('login'))
    loggedIn, firstName, noOfItems = getLoginDetails()
    return render_template("profileHome.html", loggedIn=loggedIn, firstName=firstName, noOfItems=noOfItems)

@app.route("/account/profile/edit")
def editProfile():
    if 'email' not in session:
        return redirect(url_for('login'))
    loggedIn, user_id, username = getLoginDetails()
    with sqlite3.connect('database.db') as conn:
        cur = conn.cursor()
        cur.execute("SELECT userId, email, firstName, lastName, address1, address2, zipcode, city, state, country, phone FROM users WHERE email = '" + session['email'] + "'")
        profileData = cur.fetchone()
    conn.close()
    return render_template("editProfile.html", profileData=profileData, loggedIn=loggedIn, firstName=firstName, username=username)

@app.route("/account/profile/changePassword", methods=["GET", "POST"])
def changePassword():
    if 'email' not in session:
        return redirect(url_for('login'))
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

@app.route("/account/campaigns/create", methods=["GET", "POST"])
def create_campaign():
    if 'email' not in session:
        return redirect(url_for('login'))

    loggedIn, user_id, username = getLoginDetails()

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        image = request.form['image']

        create_new_campaign(user_id, name, description)
        app.logger.info(f"\n\nName: {name} Desc: {description} Image: {image} \n\n\n")

        return url_for("account")

    else:
        return render_template("campaign_form.html")

@app.route("/account/campaigns/edit/<id>")
def edit_campaign(id):
    if 'email' not in session:
        return redirect(url_for('login'))
    return url_for('welcome')

@app.route("/maps")
def view_maps():
    return render_template("map_maker.html")

@app.route("/account/campaigns/<id>")
def view_campaign(id):
    if 'email' not in session:
        return redirect(url_for('login'))
    

@app.route("/account/characters/<char_id>")
def get_character_sheet(char_id):
    if 'email' not in session:
        return redirect(url_for('login'))

    loggedIn, user_id, username = getLoginDetails()



@app.route("/account/characters/create", methods=["GET", "POST"])
def character_creator():
    if 'email' not in session:
        return redirect(url_for('login'))


    loggedIn, user_id, username = getLoginDetails()
    if request.method == 'POST':
        # Parse form data    
        c_name = request.form['name']
        c_race = request.form['race']
        c_language = request.form['language']
        c_trait = request.form['trait']
        c_class = request.form['class']
        c_proficiency = request.form.getlist('proficiency')
        c_background = request.form['background']
        c_alignment = request.form['alignment']

        # Getting character description from form
        c_gender = request.form['gender']
        c_age = request.form['age']
        c_hgt = request.form['hgt']
        c_wgt = request.form['wgt']
        c_eye = request.form['eye']
        c_skin = request.form['skin']
        c_hair = request.form['hair']
        c_faith = request.form['faith']

        # Getting character stats from form
        c_str = request.form['str']
        c_dex = request.form['dex']
        c_con = request.form['con']
        c_int = request.form['int']
        c_wis = request.form['wis']
        c_cha = request.form['cha']

        # create stat block
        stat_block = [c_str, c_dex, c_con, c_int, c_wis, c_cha]

        # get ids
        id_race = getRaceID(c_race)
        id_class = getClassID(c_class)

        # getting other attributes based on race/class
        c_spd = getSpeed(id_race)
        c_lang = getLangKnown(id_race)
        c_start_prof = getStartingProf(id_race, id_class)
        c_hit_die = getHitDieType(id_class)
        c_prof_bonus = getProfBonus(1)

        # getting stat modifiers
        mods = convertStatsToMods(stat_block)

        str_mod = mods[0]
        dex_mod = mods[1]
        con_mod = mods[2]
        int_mod = mods[3]
        wis_mod = mods[4]
        char_mod = mods[5]

        # default dummy id values
        dummy_user = user_id
        dummy_char = 1
        # delete character
        # deleteChar(dummy_char)
        # create default character
        dummy_char = createDefaultChar(dummy_user)

        # update input values into character database
        updateName(dummy_char, c_name)
        updateCharLvl(dummy_char, 1)
        updateBackground(dummy_char, c_background)
        updateAlignment(dummy_char, c_alignment)
        updateRace(c_race, dummy_char)
        updateClass(c_class, dummy_char)
        updateProfBonus(dummy_char, c_prof_bonus)
        updateStatBlock(dummy_char, id_race, stat_block)
        updateProfBonusSkills(c_proficiency, dummy_char)
        updateProfBonusSavingThrows(dummy_char, id_class)

        # redirct to test post
        return render_template("character_sheet.html", c_name=c_name, c_race=c_race, c_class=c_class, c_background=c_background, c_alignment=c_alignment, 
        c_gender=c_gender, c_age=c_age, c_hgt=c_hgt, c_wgt=c_wgt, c_eye=c_eye, c_skin=c_skin, c_hair=c_hair, c_faith=c_faith, c_str=c_str, c_dex=c_dex, c_con=c_con,
        c_int=c_int, c_wis=c_wis, c_cha=c_cha, c_spd=c_spd, c_lang=c_lang, c_start_prof=c_start_prof, c_proficiency=c_proficiency, c_hit_die=c_hit_die,
        str_mod = str_mod, dex_mod = dex_mod, int_mod = int_mod, con_mod = con_mod, wis_mod = wis_mod, char_mod = char_mod, c_bonus=c_prof_bonus)
    
    else:
        # display the character form
        return render_template("character_form.html")


@app.route("/logout")
def logout():
    session.pop('email', None)
    return redirect(url_for('welcome'))

# def is_valid(email, password):
#     con = sqlite3.connect('database.db')
#     cur = con.cursor()
#     cur.execute('SELECT email, password FROM users')
#     data = cur.fetchall()
#     for row in data:
#         if row[0] == email and row[1] == hashlib.md5(password.encode()).hexdigest():
#             return True
#     return False


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
