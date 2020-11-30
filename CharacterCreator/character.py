from flask import *
from CharacterCreator_v1_3 import *
from CharacterGet import *
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
        dummy_user = 2
        dummy_char = 2
        # delete character
        deleteChar(dummy_char)
        createDefaultChar(dummy_user, dummy_char)

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

        # redirct to test post
        return render_template("character_sheet.html", c_name=c_name, c_race=c_race, c_class=c_class, c_background=c_background, c_alignment=c_alignment, 
        c_gender=c_gender, c_age=c_age, c_hgt=c_hgt, c_wgt=c_wgt, c_eye=c_eye, c_skin=c_skin, c_hair=c_hair, c_faith=c_faith, c_str=c_str, c_dex=c_dex, c_con=c_con,
        c_int=c_int, c_wis=c_wis, c_cha=c_cha, c_spd=c_spd, c_lang=c_lang, c_start_prof=c_start_prof, c_proficiency=c_proficiency, c_hit_die=c_hit_die,
        str_mod = str_mod, dex_mod = dex_mod, int_mod = int_mod, con_mod = con_mod, wis_mod = wis_mod, char_mod = char_mod, c_bonus=c_prof_bonus,
        str_st = str_st, dex_st = dex_st, con_st = con_st, int_st = int_st, wis_st = wis_st, char_st = char_st, c_lvl = c_lvl,
        acro = acro, anim = anim, arca = arca, athl = athl, decep = decep, hist = hist, insig = insig, intim = intim, invest = invest, 
        medi = medi, natur = natur, perc = perc, perf = perf, pers = pers, reli = reli, sleigh = sleigh, steal = steal, surv = surv)
    
    else:
        # display the character form
        return render_template("character_form.html")

# route for viewing character
@app.route('/view_character.html', methods = ['GET', 'POST'])
def view_character():
    # get all data from database
    charID = 2

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
    return render_template("character_view.html", c_name=c_name, c_race=c_race, c_class=c_class, c_background=c_background, c_alignment=c_alignment, 
    c_gender=c_gender, c_age=c_age, c_hgt=c_hgt, c_wgt=c_wgt, c_eye=c_eye, c_skin=c_skin, c_hair=c_hair, c_faith=c_faith, c_str=c_str, c_dex=c_dex, c_con=c_con,
    c_int=c_int, c_wis=c_wis, c_cha=c_cha, c_spd=c_spd, c_lang=c_lang, c_hit_die=c_hit_die, num_hit_die = num_hit_die,
    str_mod = str_mod, dex_mod = dex_mod, int_mod = int_mod, con_mod = con_mod, wis_mod = wis_mod, char_mod = char_mod, c_bonus=c_prof_bonus,
    str_st = str_st, dex_st = dex_st, con_st = con_st, int_st = int_st, wis_st = wis_st, char_st = char_st, c_lvl = c_lvl,
    acro = acro, anim = anim, arca = arca, athl = athl, decep = decep, hist = hist, insig = insig, intim = intim, invest = invest, 
    medi = medi, natur = natur, perc = perc, perf = perf, pers = pers, reli = reli, sleigh = sleigh, steal = steal, surv = surv,
    cp = cp, sp = sp, ep = ep, gp = gp, pp = pp, c_AC = c_AC, c_init = c_init, max_HP = max_HP, curr_HP = curr_HP)

# route for test post
@app.route('/character_sheet.html', methods = ['GET', 'POST'])
def character_sheet():
    # display the test post
    return render_template("character_sheet.html")

if __name__ == '__main__':
    app.run(debug=True)