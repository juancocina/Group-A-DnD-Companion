import flask
import os
from flask import *
import sqlite3, hashlib, os, requests
from numpy.lib.npyio import save
from ast import literal_eval as make_tuple
from flask import request, url_for, redirect, flash
from werkzeug.utils import secure_filename
from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from aux_functions.CharacterCreator_v1_3 import *
from aux_functions.account_queries import *
from aux_functions.campaign_creator import *
from aux_functions.CharacterGet import *
from aux_functions.map_maker import *
# from aux_functions.UpdateCharacter import *
#from config import Config

app = flask.Flask(__name__)
app.config.from_envvar('APP_CONFIG')
app.secret_key = app.config['SECRET_KEY']

registration_required = app.config['REGISTER_USER_REQUIRED']

login = LoginManager()

DATABASE_USERS = app.config['DATABASE_USERS']
DATABASE_CHARACTER = app.config['DATABASE_CHARACTER']
CAMPAIGN_IMAGES = app.config['CAMPAIGN_IMAGES']

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

    LoggedIn = True

    if 'email' not in session:
        LoggedIn = False

    return render_template('welcome.html', LoggedIn=LoggedIn)



# LOGIN AND REGISTRATION ROUTES #
#################################

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


# Account and Profile Routes #
##############################

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


# Campaigns Routes #
####################

@app.route("/account/campaigns/create", methods=["GET", "POST"])
def create_campaign():
    if 'email' not in session:
        return redirect(url_for('login'))

    loggedIn, user_id, username = getLoginDetails()

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        c_id = create_new_campaign(user_id, name, description)
        if 'image' not in request.files:
            pass
        else:
            image = request.files['image']
            if not os.path.exists(CAMPAIGN_IMAGES+str(c_id)):
                os.makedirs(CAMPAIGN_IMAGES+str(c_id))
            filename = image.filename
            savepath = os.path.join(CAMPAIGN_IMAGES+str(c_id), filename)
            image.save(savepath)

            update_campaign_cover(c_id, filename)



        
        return redirect(url_for("account"))

    else:
        return render_template("campaign_form.html")


# # Map Maker #
@app.route("/account/campaigns/<id>/maps/create", methods=["GET", "POST"])
def make_map(id):
    if 'email' not in session:
        return redirect(url_for('login'))

    loggedIn, user_id, username = getLoginDetails()

    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        environment = request.form['environment']
        shape = request.form['shape']
        scale = request.form['scale']
        octaves = request.form['octaves']


        if shape == "small":
            shape = (400, 400)
        elif shape == "medium":
            shape = (800, 800)
        elif shape == "large":
            shape = (1200, 1200)

        scale = int(scale)
        octaves = int(octaves)
        persistence = 0.5
        lacunarity = 2

        # options_dict = {"name": name, "description": description, "environment": environment, "shape": shape, "scale": scale, "octaves": octaves}

        # obj = map_config(options_dict)

        filename = name+".png"
        savepath = os.path.join(CAMPAIGN_IMAGES+str(id), filename)

        world = make_world(shape, scale, octaves, persistence, lacunarity)


        if environment == "desert":
            color_world = color_desert(world, app.config['DESERT_COLOR'], shape, savepath)
        elif environment == "islands":
            color_world = color_islands(world, app.config['ISLANDS_COLOR'], shape, savepath)
        elif environment == "caves":
            color_world = color_caves(world, app.config['CAVES_COLOR'], shape, savepath)
        elif environment == "forest":
            color_world = color_forest(world, app.config['FORESTS_COLOR'], shape, savepath)
        elif environment == "blossom":
            color_wold = color_blossom(world, app.config['BLOSSOM_COLOR'], shape, savepath)
        elif environment == "terrace":
            color_world = color_terrace(world, app.config['TERRACE_COLOR'], shape, savepath)
        else:
            pass

        final = add_grid(savepath, environment)


        save_grid(name, description, id, filename)

        return redirect(url_for('account'))

    else:
        return render_template("map_maker.html", id=id)



@app.route("/account/campaigns/<id>/edit")
def edit_campaign(id):
    if 'email' not in session:
        return redirect(url_for('login'))

    return url_for('welcome')

@app.route("/account/campaigns/<id>/delete")
def delete_campaign(id):
    if 'email' not in session:
        return redirect(url_for('login'))
    delete_account_campaign(id)

    return redirect(url_for('account'))



@app.route("/account/campaigns/<id>")
def view_campaign(id):
    if 'email' not in session:
        return redirect(url_for('login'))

    c_data, m_data = query_campaign(id)

    app.logger.info(f"\n\n\n Campaign Data: {c_data}  Map Data: {m_data}")
    return render_template("campaign_view.html", id=id, c_data=c_data, m_data=m_data)

    

# Characters Routes #
#####################
@app.route("/account/characters")
def get_characters():
    if 'email' not in session:
        return redirect(url_for('login'))

    loggedIn, user_id, username = getLoginDetails()

    characters = query_account_characters(user_id)

    return render_template("characters_list.html", characters=characters)



    


@app.route("/account/characters/<char_id>/delete")
def delete_character(char_id):
    if 'email' not in session:
        return redirect(url_for('login'))

    loggedIn, user_id, username = getLoginDetails()
    deleteChar(char_id)
    return redirect(url_for('account'))

@app.route("/account/characters/<char_id>")
def get_character_sheet(char_id):
    if 'email' not in session:
        return redirect(url_for('login'))

    loggedIn, user_id, username = getLoginDetails()

    gameview = session['gameview']

    charID = char_id
    # get character info
    character = getCharacter(charID)
    c_name = character[2]
    c_lvl = character[3]
    c_race = getRace(character[4])
    c_class = getClass(character[5])
    c_background = character[6]
    c_alignment = character[7]
    c_prof_bonus = character[8]
    c_AC = character[9]
    c_init = character[10]
    c_spd = character[11]
    max_HP = character[12]
    c_hit_die = character[13]
    num_hit_die = character[14]
    curr_HP = character[15]

    # get descriptors
    descriptors = getDescriptors(charID)
    c_age = descriptors[1]
    c_hgt = descriptors[2]
    c_wgt = descriptors[3]
    c_eye = descriptors[4]
    c_skin = descriptors[5]
    c_hair = descriptors[6]
    c_gender = descriptors[7]
    c_faith = descriptors[8]

    # get proficiencies
    proficiencies = getProficiencies(charID)
    lang = proficiencies[5]
    no_bracket = lang[1:-1]
    no_quote = no_bracket.replace("\'", "")
    c_lang = no_quote.split(', ')

    # get saving throws
    savingThrows = getSavings(charID)
    str_st = savingThrows[1]
    dex_st = savingThrows[2]
    con_st = savingThrows[3]
    int_st = savingThrows[4]
    wis_st = savingThrows[5]
    char_st = savingThrows[6]

    # get skills
    skills = getSkills(charID)
    acro = skills[1]
    anim = skills[2]
    arca = skills[3]
    athl = skills[4]
    decep = skills[5]
    hist = skills[6]
    insig = skills[7]
    intim = skills[8]
    invest = skills[9]
    medi = skills[10]
    natur = skills[11]
    perc = skills[12]
    perf = skills[13]
    pers = skills[14]
    reli = skills[15]
    sleigh = skills[16]
    steal = skills[17]
    surv = skills[18]

    # get stat block
    statblock = getStatBlock(charID)
    c_str = statblock[1]
    c_dex = statblock[2]
    c_con = statblock[3]
    c_int = statblock[4]
    c_wis = statblock[5]
    c_cha = statblock[6]

    stat_block = [c_str, c_dex, c_con, c_int, c_wis, c_cha]

    # getting stat modifiers
    mods = convertStatsToMods(stat_block)

    str_mod = mods[0]
    dex_mod = mods[1]
    con_mod = mods[2]
    int_mod = mods[3]
    wis_mod = mods[4]
    char_mod = mods[5]

    # dummy values
    c_spd = 0

    # get currency
    currency = getCurrency(charID)
    cp = currency[1]
    sp = currency[2]
    ep = currency[3]
    gp = currency[4]
    pp = currency[5]
 
    # redirct to test post
    return render_template("character_sheet.html", c_name=c_name, c_race=c_race, c_class=c_class, c_background=c_background, c_alignment=c_alignment, 
    c_gender=c_gender, c_age=c_age, c_hgt=c_hgt, c_wgt=c_wgt, c_eye=c_eye, c_skin=c_skin, c_hair=c_hair, c_faith=c_faith, c_str=c_str, c_dex=c_dex, c_con=c_con,
    c_int=c_int, c_wis=c_wis, c_cha=c_cha, c_spd=c_spd, c_lang=c_lang, c_hit_die=c_hit_die, num_hit_die = num_hit_die,
    str_mod = str_mod, dex_mod = dex_mod, int_mod = int_mod, con_mod = con_mod, wis_mod = wis_mod, char_mod = char_mod, c_bonus=c_prof_bonus,
    str_st = str_st, dex_st = dex_st, con_st = con_st, int_st = int_st, wis_st = wis_st, char_st = char_st, c_lvl = c_lvl,
    acro = acro, anim = anim, arca = arca, athl = athl, decep = decep, hist = hist, insig = insig, intim = intim, invest = invest, 
    medi = medi, natur = natur, perc = perc, perf = perf, pers = pers, reli = reli, sleigh = sleigh, steal = steal, surv = surv,
    cp = cp, sp = sp, ep = ep, gp = gp, pp = pp, c_AC = c_AC, c_init = c_init, max_HP = max_HP, curr_HP = curr_HP, loggedIn=loggedIn, gameview=gameview)


@app.route("/account/characters/create", methods=["GET", "POST"])
def character_creator():
    if 'email' not in session:
        return redirect(url_for('login'))


    loggedIn, user_id, username = getLoginDetails()
    if request.method == 'POST':
        # Parse form data    
        c_name = request.form['name']
        c_race = request.form['race']
        c_class = request.form['class']
        c_proficiency = request.form.getlist('proficiency')
        c_background = request.form['background']
        c_alignment = request.form['alignment']

        c_lvl = 1

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

        # calculate saving throws stats
        str_st = str_mod
        dex_st = dex_mod
        con_st = con_mod
        int_st = int_mod
        wis_st = wis_mod
        char_st = char_mod

        if (c_class == "Barbarian"):
            str_st += c_prof_bonus
            con_st += c_prof_bonus
        elif (c_class == "Bard"):
            dex_st += c_prof_bonus
            char_st += c_prof_bonus
        elif (c_class == "Cleric"):
            wis_st += c_prof_bonus
            char_st += c_prof_bonus
        elif (c_class == "Druid"):
            int_st += c_prof_bonus
            wis_st += c_prof_bonus
        elif (c_class == "Fighter"):
            str_st += c_prof_bonus
            con_st += c_prof_bonus
        elif (c_class == "Monk"):
            str_st += c_prof_bonus
            dex_st += c_prof_bonus
        elif (c_class == "Paladin"):
            wis_st += c_prof_bonus
            char_st += c_prof_bonus
        elif (c_class == "Ranger"):
            str_st += c_prof_bonus
            dex_st += c_prof_bonus
        elif (c_class == "Rogue"):
            dex_st += c_prof_bonus
            int_st += c_prof_bonus
        elif (c_class == "Sorcerer"):
            con_st += c_prof_bonus
            char_st += c_prof_bonus
        elif (c_class == "Warlock"):
            wis_st += c_prof_bonus
            char_st += c_prof_bonus
        elif (c_class == "Wizard"):
            int_st += c_prof_bonus
            wis_st += c_prof_bonus
        
        # calculate skill bonuses
        acro = dex_mod
        anim = wis_mod
        arca = int_mod
        athl = str_mod
        decep = char_mod
        hist = int_mod
        insig = wis_mod
        intim = char_mod
        invest = int_mod
        medi = wis_mod
        natur = int_mod
        perc = wis_mod
        perf = char_mod
        pers = char_mod
        reli = int_mod
        sleigh = dex_mod
        steal = dex_mod
        surv = wis_mod

        for prof in c_proficiency:
            if (prof == "Skill: Acrobatics"):
                acro += c_prof_bonus
            elif (prof == "Skill: Animal Handling"):
                anim += c_prof_bonus
            elif (prof == "Skill: Arcana"):
                arca += c_prof_bonus
            elif (prof == "Skill: Athletics"):
                athl += c_prof_bonus
            elif (prof == "Skill: Deception"):
                decep += c_prof_bonus
            elif (prof == "Skill: History"):
                hist += c_prof_bonus
            elif (prof == "Skill: Insight"):
                insig += c_prof_bonus
            elif (prof == "Skill: Intimidation"):
                intim += c_prof_bonus
            elif (prof == "Skill: Investigation"):
                invest += c_prof_bonus
            elif (prof == "Skill: Medicine"):
                medi += c_prof_bonus
            elif (prof == "Skill: Nature"):
                natur += c_prof_bonus
            elif (prof == "Skill: Perception"):
                perc += c_prof_bonus
            elif (prof == "Skill: Performance"):
                perf += c_prof_bonus
            elif (prof == "Skill: Persuasion"):
                pers += c_prof_bonus
            elif (prof == "Skill: Religion"):
                reli += c_prof_bonus
            elif (prof == "Skill: Sleight of Hand"):
                sleigh += c_prof_bonus
            elif (prof == "Skill: Stealth"):
                steal += c_prof_bonus
            elif (prof == "Skill: Survival"):
                surv += c_prof_bonus

        # create empty character in database
        dummy_user = user_id
        # delete character
        # deleteChar(dummy_char)
        # create default character
        dummy_char = createDefaultChar(dummy_user)

        # update input values into character database
        updateName(dummy_char, c_name)
        updateCharLvl(dummy_char, c_lvl)
        updateBackground(dummy_char, c_background)
        updateAlignment(dummy_char, c_alignment)
        updateRace(c_race, dummy_char)
        updateClass(c_class, dummy_char)
        updateProfBonus(dummy_char, c_prof_bonus)
        updateStatBlock(dummy_char, id_race, stat_block)
        updateProfBonusSkills(c_proficiency, dummy_char)
        updateProfBonusSavingThrows(dummy_char, id_class)
        updateDescriptors(dummy_char, c_age, c_hgt, c_wgt, c_eye, c_skin, c_hair, c_gender, c_faith)

        return redirect(url_for('get_character_sheet', char_id=dummy_char))

        # redirct to test post
        # return render_template("character_sheet.html", c_name=c_name, c_race=c_race, c_class=c_class, c_background=c_background, c_alignment=c_alignment, 
        # c_gender=c_gender, c_age=c_age, c_hgt=c_hgt, c_wgt=c_wgt, c_eye=c_eye, c_skin=c_skin, c_hair=c_hair, c_faith=c_faith, c_str=c_str, c_dex=c_dex, c_con=c_con,
        # c_int=c_int, c_wis=c_wis, c_cha=c_cha, c_spd=c_spd, c_lang=c_lang, c_start_prof=c_start_prof, c_proficiency=c_proficiency, c_hit_die=c_hit_die,
        # str_mod = str_mod, dex_mod = dex_mod, int_mod = int_mod, con_mod = con_mod, wis_mod = wis_mod, char_mod = char_mod, c_bonus=c_prof_bonus,
        # str_st = str_st, dex_st = dex_st, con_st = con_st, int_st = int_st, wis_st = wis_st, char_st = char_st, c_lvl = c_lvl,
        # acro = acro, anim = anim, arca = arca, athl = athl, decep = decep, hist = hist, insig = insig, intim = intim, invest = invest, 
        # medi = medi, natur = natur, perc = perc, perf = perf, pers = pers, reli = reli, sleigh = sleigh, steal = steal, surv = surv)
    
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

@app.route("/game/<id>")
def game_view(id):
    session['gameview'] = True

    c_data, m_data = query_campaign(id)


    return render_template("game_view.html", id=id, c_data=c_data, m_data=m_data)


@app.route("/dice")
def dice():
    return render_template("dice2.html")

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
