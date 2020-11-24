from flask import *
from CharacterCreator_v1_3 import *
import sqlite3, hashlib, os
from werkzeug.utils import secure_filename

app = Flask(__name__)

# route for home page
@app.route('/', methods = ['GET', 'POST'])
def home_page():
    # display home page
    return render_template("home_page.html")

# route for character form
@app.route('/character_form.html', methods = ['GET', 'POST'])
def character_form():
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

        # # create empty character in database
        # dummy_user = 1
        # dummy_char = 1
        # createDefaultChar(dummy_user, dummy_char)

        # update input values into character database
        # updateName(dummy_char, c_name)
        # updateCharLvl(dummy_char, 1)
        # updateBackground(dummy_char, c_background)
        # updateAlignment(dummy_char, c_alignment)
        # updateRace(c_race, dummy_char)
        # updateClass(c_class, dummy_char)
        # updateStatBlock(dummy_char, id_race, stat_block)
        # convertStatsToMods(stat_block)
        # updateSavingThrows(dummy_char, stat_block)
        # updateSkills(dummy_char, stat_block)
        # updateProfBonusSkills(c_proficiency, dummy_char)
        # updateProfBonusSavingThrows(dummy_char, id_class)
        # updateProfBonus(dummy_char, c_prof_bonus)

        # delete character
        #deleteChar(dummy_char)


        # redirct to test post
        return render_template("character_sheet.html", c_name=c_name, c_race=c_race, c_class=c_class, c_background=c_background, c_alignment=c_alignment, 
        c_gender=c_gender, c_age=c_age, c_hgt=c_hgt, c_wgt=c_wgt, c_eye=c_eye, c_skin=c_skin, c_hair=c_hair, c_faith=c_faith, c_str=c_str, c_dex=c_dex, c_con=c_con,
        c_int=c_int, c_wis=c_wis, c_cha=c_cha, c_spd=c_spd, c_lang=c_lang, c_start_prof=c_start_prof, c_proficiency=c_proficiency, c_hit_die=c_hit_die)
    
    else:
        # display the character form
        return render_template("character_form.html")

# route for test post
@app.route('/character_sheet.html', methods = ['GET', 'POST'])
def character_sheet():
    # display the test post
    return render_template("character_sheet.html")

if __name__ == '__main__':
    app.run(debug=True)