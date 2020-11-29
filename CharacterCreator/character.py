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
        dummy_user = 2
        dummy_char = 2
        # delete character
        deleteChar(dummy_char)
        createDefaultChar(dummy_user, dummy_char)

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
        str_mod = str_mod, dex_mod = dex_mod, int_mod = int_mod, con_mod = con_mod, wis_mod = wis_mod, char_mod = char_mod, c_bonus=c_prof_bonus,
        str_st = str_st, dex_st = dex_st, con_st = con_st, int_st = int_st, wis_st = wis_st, char_st = char_st,
        acro = acro, anim = anim, arca = arca, athl = athl, decep = decep, hist = hist, insig = insig, intim = intim, invest = invest, 
        medi = medi, natur = natur, perc = perc, perf = perf, pers = pers, reli = reli, sleigh = sleigh, steal = steal, surv = surv)
    
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