# Author:  Manuel Perez
# Date:    10/05/2020
# Purpose: This is our character creator
#
####################################################################
# import some libraries
import sqlite3

CHARACTER_DB = '../database/db/DnDEZ_Character.db'
CLASS_DB = '../database/db/DnDEZ_Class.db'
RACE_DB = '../database/db/DnDEZ_Race.db'


# open a connection to our db and create a cursor
conn = sqlite3.connect(CHARACTER_DB, check_same_thread=False)
c = conn.cursor()

# Functions ########################################################
# create default char
def createDefaultChar(id):
    # set ID's
    userID = id
    
    # set all the info in user_char_list
    charName = 'n/a'
    charLvl = 1
    raceID = 'n/a'
    classID = 'n/a'
    backgroundID = 'n/a'
    alignment = 'n/a'
    profBonus = 2
    AC = 10
    initiative = 0
    speed = 0
    max_hp = 0
    hit_die_type = 'n/a'
    num_hit_die = charLvl
    curr_hp = 0
    

    newCharList = [userID, charName,
                   charLvl, raceID, classID,
                   backgroundID, alignment, profBonus,
                   AC, initiative, speed, max_hp,
                   hit_die_type, num_hit_die, curr_hp]

    # insert into char list table
    c.execute("INSERT INTO user_character_list (\"user_id\", \"char_name\", \"char_lvl\", \"race_id\", \"class_id\", \"background_id\", \"alignment\", \"prof_bonus\", \"AC\", \"initiative\", \"speed\", \"max_hp\", \"hit_die_type\", \"num_hit_die\", \"curr_hp\") VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)", (userID, charName,charLvl, raceID, classID, backgroundID, alignment, profBonus, AC, initiative, speed, max_hp, hit_die_type, num_hit_die, curr_hp))
    conn.commit()

    sql = '''SELECT char_id FROM user_character_list WHERE user_id=? AND char_name=?'''
    c.execute(sql, (userID, 'n/a'))
    data = c.fetchall()[0][0]

    charID = data

    # default stat block to 0's
    strength = 0
    dexterity = 0
    constitution = 0
    intelligence = 0
    wisdom = 0
    charisma = 0
    
    statBlock = [charID, strength, dexterity, constitution, 
                 intelligence, wisdom, charisma]
    
    # insert into skill table
    sql = '''INSERT INTO char_stat_block VALUES 
    (?,?,?,?,?,?,?)'''
    c.execute(sql, statBlock)
    conn.commit()
    
    # default skill block
    acrobatics = 0
    animalHandling = 0
    arcana = 0
    athletics = 0
    deception = 0
    history = 0
    insight = 0
    intimidation = 0
    investigation = 0
    medicine = 0
    nature = 0
    perception = 0
    performance = 0
    persuasion = 0
    religion = 0
    sleightOfHand = 0
    stealth = 0
    survival = 0
    
    skillList = [charID, acrobatics, animalHandling, 
                arcana, athletics, deception, history,
                insight, intimidation, investigation,
                medicine, nature, perception,
                performance, persuasion, religion,
                sleightOfHand, stealth, survival]
    
    # insert into skill table
    sql = '''INSERT INTO char_skill_list VALUES 
    (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
    c.execute(sql, skillList)
    conn.commit()
    
    strSaving = 0
    dexSaving = 0
    conSaving = 0
    intSaving = 0
    wisSaving = 0
    chaSaving = 0
    
    savingThrowList = [charID, strSaving, dexSaving, conSaving,
                       intSaving, wisSaving, chaSaving]
    
    # insert into char list table
    sql = '''INSERT INTO char_saving_throws VALUES 
    (?,?,?,?,?,?,?)'''
    c.execute(sql, savingThrowList)
    conn.commit()    
    


    cp = 0
    sp = 0
    ep = 0
    gp = 0
    pp = 0
    
    currencyList = [charID, cp, sp, ep, gp, pp]
    
    # insert into currency
    sql = '''INSERT INTO char_currency VALUES 
    (?,?,?,?,?,?)'''
    c.execute(sql, currencyList)
    conn.commit()

    armorProf = 'n/a'
    weaponProf = 'n/a'
    shieldProf = 'n/a'
    toolProf = 'n/a'
    languages = 'n/a'
    
    profList = [charID, armorProf, weaponProf, 
                shieldProf, toolProf, languages]
    
    # insert prof
    sql = '''INSERT INTO char_proficiencies VALUES 
    (?,?,?,?,?,?)'''
    c.execute(sql, profList)
    conn.commit()

    age = 'n/a'
    height = 'n/a'
    weight = 'n/a'
    eyes = 'n/a'
    skin = 'n/a'
    hair = 'n/a'
    gender = 'n/a'
    faith = 'n/a'

    descriptors = [charID, age, height, weight, eyes, skin, hair, gender, faith]

    # insert descriptors
    sql = '''INSERT INTO char_descriptors VALUES 
    (?,?,?,?,?,?,?,?,?)'''
    c.execute(sql, descriptors)
    conn.commit()

    return charID
    
def getRaceID(raceName):
    # open race db
    tempConn = sqlite3.connect(RACE_DB)
    tempC = tempConn.cursor()
    
    # retrieve the race_id by using race_name
    tempC.execute('SELECT race_id FROM race WHERE race_name = ?', [raceName])
    data = tempC.fetchone()
    
    # close race db
    tempC.close()
    tempConn.close()
    
    return data[0]

def getRace(raceID):
    # open race db
    tempConn = sqlite3.connect(RACE_DB)
    tempC = tempConn.cursor()
    
    # retrieve the race_id by using race_name
    tempC.execute('SELECT race_name FROM race WHERE race_id = ?', [raceID])
    data = tempC.fetchone()
    
    # close race db
    tempC.close()
    tempConn.close()
    
    return data[0]

def getClassID(className):
    # open class db
    tempConn = sqlite3.connect(CLASS_DB)
    tempC = tempConn.cursor()
    
    # retrieve the race_id by using race_name
    tempC.execute('SELECT class_id FROM class WHERE class_name = ?', [className])
    data = tempC.fetchone()
    
    # close race db
    tempC.close()
    tempConn.close()
    
    return data[0]

def getClass(classID):
    # open class db
    tempConn = sqlite3.connect(CLASS_DB)
    tempC = tempConn.cursor()
    
    # retrieve the race_id by using race_name
    tempC.execute('SELECT class_name FROM class WHERE class_id = ?', [classID])
    data = tempC.fetchone()
    
    # close race db
    tempC.close()
    tempConn.close()
    
    return data[0]

def getSpeed(raceID): 
    # open race db
    tempConn = sqlite3.connect(RACE_DB)
    tempC = tempConn.cursor()
    
    # retrieve the race_id by using race_name
    tempC.execute('SELECT speed FROM race WHERE race_id = ?', [raceID])
    data = tempC.fetchone()
    
    # close race db
    tempC.close()
    tempConn.close()
    
    return data[0]

def getLvl(charID):
    # retrieve the race_id by using race_name
    c.execute('SELECT char_lvl FROM user_character_list WHERE char_id = ?', [charID])
    data = c.fetchone()
    
    return data[0]

def getLangKnown(raceID):
    # open race db
    tempConn = sqlite3.connect(RACE_DB)
    tempC = tempConn.cursor()
    
    # retrieve the langids from languages known
    tempC.execute('SELECT lang_id FROM languages_known WHERE race_id = ?', [raceID])
    data = tempC.fetchall()
    
    # retrive the languages using lang ids
    langsKnown = []
    for langIndex in data:
        tempC.execute('''SELECT lang FROM languages WHERE lang_id = ?''', langIndex)
        langData = tempC.fetchone()
        langsKnown.append(langData[0])
        
    # close race db
    tempC.close()
    tempConn.close()
    
    return langsKnown

def getStartingProf(raceID, classID):
    profList = []
    
    # open race db
    tempConn = sqlite3.connect(RACE_DB)
    tempC = tempConn.cursor()
    
    # retrieve the prof by using race_id
    tempC.execute('SELECT proficiency FROM starting_prof WHERE race_id = ?', [raceID])
    data = tempC.fetchall()
    
    for dataIndex in data:
        profList.append(dataIndex[0])
    
    # close race db
    tempC.close()
    tempConn.close()
    
    # open class db
    tempConn = sqlite3.connect(CLASS_DB)
    tempC = tempConn.cursor()
    
    # retrieve the r by using class id
    tempC.execute('SELECT prof_name FROM prof_known WHERE class_id = ?', [classID])
    data = tempC.fetchall()
    
    for dataIndex in data:
        profList.append(dataIndex[0])
    
    # close class db
    tempC.close()
    tempConn.close()
    
    return profList
    
def getTraitsKnown(raceID):
    print('temp')
    
def getHitDieType(classID):
    # open class db
    tempConn = sqlite3.connect(CLASS_DB)
    tempC = tempConn.cursor()
    
    # retrieve the hitdietype by using class_id
    tempC.execute('SELECT hit_die FROM class WHERE class_id = ?', [classID])
    data = tempC.fetchone()
    
    # close race db
    tempC.close()
    tempConn.close()
    
    return data[0]
    
def updateName(charID, charName):
    # update char name
    sql = '''UPDATE user_character_list SET char_name = ? WHERE char_id = ?'''        
    data = (charName, charID)
    c.execute(sql, data)
    conn.commit()
    
def updateCharLvl(charID, lvl):
    # update char lvl
    sql = '''UPDATE user_character_list SET char_lvl = ? WHERE char_id = ?'''        
    data = (lvl, charID)
    c.execute(sql, data)
    conn.commit()
    
    # update num of hit die
    sql = '''UPDATE user_character_list SET num_hit_die = ? WHERE char_id = ?'''        
    data = (lvl, charID)
    c.execute(sql, data)
    conn.commit()

def updateBackground(charID, background):
    # update background
    sql = '''UPDATE user_character_list SET background_id = ? WHERE char_id = ?'''        
    data = (background, charID)
    c.execute(sql, data)
    conn.commit()
    
def updateAlignment(charID, alignment):
    # update alignment
    sql = '''UPDATE user_character_list SET alignment = ? WHERE char_id = ?'''        
    data = (alignment, charID)
    c.execute(sql, data)
    conn.commit()

def updateProfBonus(charID, profBon):
    # update prof bon
    sql = '''UPDATE user_character_list SET prof_bonus = ? WHERE char_id = ?'''        
    data = (profBon, charID)
    c.execute(sql, data)
    conn.commit()

def updateAC(charID, ac):
    # update prof bon
    sql = '''UPDATE user_character_list SET AC = ? WHERE char_id = ?'''        
    data = (ac, charID)
    c.execute(sql, data)
    conn.commit()

def updateInitiative(charID, initiative):
    # update initiative
    sql = '''UPDATE user_character_list SET initiative = ? WHERE char_id = ?'''        
    data = (initiative, charID)
    c.execute(sql, data)
    conn.commit()

def updateHP(charID, hp):
    # update hp
    sql = '''UPDATE user_character_list SET max_hp = ? WHERE char_id = ?'''        
    data = (hp, charID)
    c.execute(sql, data)
    conn.commit()

def updateCurrHP(charID, hp):
    # update hp
    sql = '''UPDATE user_character_list SET curr_hp = ? WHERE char_id = ?'''        
    data = (hp, charID)
    c.execute(sql, data)
    conn.commit()
    
def updateRace(raceName, charID):
    # update race_id
    raceID = getRaceID(raceName)
    sql = '''UPDATE user_character_list SET race_id = ? WHERE char_id = ?'''        
    data = (raceID, charID)
    c.execute(sql, data)
    conn.commit()
    
    # update speed
    speed = getSpeed(raceID)
    sql = '''UPDATE user_character_list SET speed = ? WHERE char_id = ?'''        
    data = (speed, charID)
    c.execute(sql, data)
    conn.commit()
    
    # update languages known
    langList = getLangKnown(raceID)
    sql = '''UPDATE char_proficiencies SET languages = ? WHERE char_id = ?'''        
    data = (str(langList), charID)
    c.execute(sql, data)
    conn.commit()
    
    # update traits known
def updateClass(className, charID):
    # update class_id
    classID = getClassID(className)
    sql = '''UPDATE user_character_list SET class_id = ? WHERE char_id = ?'''        
    data = (classID, charID)
    c.execute(sql, data)
    conn.commit()
    
    # update hit die type
    hitDie = getHitDieType(classID)
    sql = '''UPDATE user_character_list SET hit_die_type = ? WHERE char_id = ?'''        
    data = (hitDie, charID)
    c.execute(sql, data)
    conn.commit()
    
# update stat block
def updateStatBlock(charID, raceID, statBlock):
    # open race db
    tempConn = sqlite3.connect(RACE_DB)
    tempC = tempConn.cursor()
    
    # retrieve the bonus type and unit using race_id
    tempC.execute('SELECT stat_name, bonus FROM stat_bonuses WHERE race_id = ?', [raceID])
    bonusData = tempC.fetchall()

    temp = []

    for stat in statBlock:
        int_var = int(stat)
        temp.append(int_var)
    
    # update the statblock stats
    for row in bonusData:
        if row[0] == 'STR':
            temp[0] += row[1]
        elif row[0] == 'DEX':
            temp[1] += row[1]
        elif row[0] == 'CON':
            temp[2] += row[1]
        elif row[0] == 'INT':
            temp[3] += row[1]
        elif row[0] == 'WIS':
            temp[4] += row[1]
        elif row[0] == 'CHA':
            temp[5] += row[1]
        else:
            print("error - unkown type") 
    
    statBlock = temp
    
    # close out our cursor 
    tempC.close()
    tempConn.close()
    
    # update statblock table ####################################################
    # update str
    sql = '''UPDATE char_stat_block SET strength = ? WHERE char_id = ?'''        
    data = (statBlock[0], charID)
    c.execute(sql, data)
    conn.commit()
    
    # update dex
    sql = '''UPDATE char_stat_block SET dexterity = ? WHERE char_id = ?'''        
    data = (statBlock[1], charID)
    c.execute(sql, data)
    conn.commit()
    
    # update con
    sql = '''UPDATE char_stat_block SET constitution = ? WHERE char_id = ?'''        
    data = (statBlock[2], charID)
    c.execute(sql, data)
    conn.commit()
    
    # update int
    sql = '''UPDATE char_stat_block SET intelligence = ? WHERE char_id = ?'''        
    data = (statBlock[3], charID)
    c.execute(sql, data)
    conn.commit()
    
    # update wis
    sql = '''UPDATE char_stat_block SET wisdom = ? WHERE char_id = ?'''        
    data = (statBlock[4], charID)
    c.execute(sql, data)
    conn.commit()
    
    # update cha
    sql = '''UPDATE char_stat_block SET charisma = ? WHERE char_id = ?'''        
    data = (statBlock[5], charID)
    c.execute(sql, data)
    conn.commit()
    
    # convert the stats into mods and update skills and saving throws
    temp = convertStatsToMods(statBlock)
    updateSkills(charID, temp)
    updateSavingThrows(charID, temp)
    
def convertStatsToMods(statBlock):

    temp = []

    for stat in statBlock:
        int_var = int(stat)
        temp.append(int_var)

    sbIndex = 0
    
    for index in temp:
        if index == 1:
            temp[sbIndex] = -5
        elif index == 2 or index == 3:
            temp[sbIndex] = -4
        elif index == 4 or index == 5:
            temp[sbIndex] = -3
        elif index == 6 or index == 7:
            temp[sbIndex] = -2
        elif index == 8 or index == 9:
            temp[sbIndex] = -1
        elif index == 10 or index == 11:
            temp[sbIndex] = 0
        elif index == 12 or index == 13:
            temp[sbIndex] = 1
        elif index == 14 or index == 15:
            temp[sbIndex] = 2
        elif index == 16 or index == 17:
            temp[sbIndex] = 3
        elif index == 18 or index == 19:
            temp[sbIndex] = 4 
        elif index >= 20:
            temp[sbIndex] = 5
        
        sbIndex += 1

    return temp

def updateSavingThrows(charID, statBlock):
    # update str saving throw
    sql = '''UPDATE char_saving_throws SET str_saving = ? WHERE char_id = ?'''        
    data = (statBlock[0], charID)
    c.execute(sql, data)
    conn.commit()
    # update dex saving throw
    sql = '''UPDATE char_saving_throws SET dex_saving = ? WHERE char_id = ?'''        
    data = (statBlock[1], charID)
    c.execute(sql, data)
    conn.commit()
    
    # update con saving throw
    sql = '''UPDATE char_saving_throws SET con_saving = ? WHERE char_id = ?'''        
    data = (statBlock[2], charID)
    c.execute(sql, data)
    conn.commit()
    
    # update int saving throw
    sql = '''UPDATE char_saving_throws SET int_saving = ? WHERE char_id = ?'''        
    data = (statBlock[3], charID)
    c.execute(sql, data)
    conn.commit()
    
    # update wis saving throw
    sql = '''UPDATE char_saving_throws SET wis_saving = ? WHERE char_id = ?'''        
    data = (statBlock[4], charID)
    c.execute(sql, data)
    conn.commit()
    
    # update cha saving throw
    sql = '''UPDATE char_saving_throws SET cha_saving = ? WHERE char_id = ?'''        
    data = (statBlock[5], charID)
    c.execute(sql, data)
    conn.commit()
    
def updateSkills(charID, statBlock):    
    # update all str based skills
    sql = '''UPDATE char_skill_list SET athletics = ? WHERE char_id = ?'''        
    data = (statBlock[0], charID)
    c.execute(sql, data)
    conn.commit()
    
    # update all dex based skills
    sql = '''UPDATE char_skill_list SET acrobatics = ? WHERE char_id = ?'''        
    data = (statBlock[1], charID)
    c.execute(sql, data)
    conn.commit()
    
    sql = '''UPDATE char_skill_list SET sleight_of_hand = ? WHERE char_id = ?'''        
    data = (statBlock[1], charID)
    c.execute(sql, data)
    conn.commit()
    
    sql = '''UPDATE char_skill_list SET stealth = ? WHERE char_id = ?'''        
    data = (statBlock[1], charID)
    c.execute(sql, data)
    conn.commit()
       
    # update all int based skills
    sql = '''UPDATE char_skill_list SET arcana = ? WHERE char_id = ?'''        
    data = (statBlock[3], charID)
    c.execute(sql, data)
    conn.commit()
    
    sql = '''UPDATE char_skill_list SET history = ? WHERE char_id = ?'''        
    data = (statBlock[3], charID)
    c.execute(sql, data)
    conn.commit()
    
    sql = '''UPDATE char_skill_list SET investigation = ? WHERE char_id = ?'''        
    data = (statBlock[3], charID)
    c.execute(sql, data)
    conn.commit()
    
    sql = '''UPDATE char_skill_list SET nature = ? WHERE char_id = ?'''        
    data = (statBlock[3], charID)
    c.execute(sql, data)
    conn.commit()
    
    sql = '''UPDATE char_skill_list SET religion = ? WHERE char_id = ?'''        
    data = (statBlock[3], charID)
    c.execute(sql, data)
    conn.commit()
    
    # update all wis based skills
    sql = '''UPDATE char_skill_list SET animal_handling = ? WHERE char_id = ?'''        
    data = (statBlock[4], charID)
    c.execute(sql, data)
    conn.commit()
    
    sql = '''UPDATE char_skill_list SET insight = ? WHERE char_id = ?'''        
    data = (statBlock[4], charID)
    c.execute(sql, data)
    conn.commit()
    
    sql = '''UPDATE char_skill_list SET medicine = ? WHERE char_id = ?'''        
    data = (statBlock[4], charID)
    c.execute(sql, data)
    conn.commit()
    
    sql = '''UPDATE char_skill_list SET perception = ? WHERE char_id = ?'''        
    data = (statBlock[4], charID)
    c.execute(sql, data)
    conn.commit()
    
    sql = '''UPDATE char_skill_list SET survival = ? WHERE char_id = ?'''        
    data = (statBlock[4], charID)
    c.execute(sql, data)
    conn.commit()
    
    # update all cha based skills
    sql = '''UPDATE char_skill_list SET deception = ? WHERE char_id = ?'''        
    data = (statBlock[5], charID)
    c.execute(sql, data)
    conn.commit()
    
    sql = '''UPDATE char_skill_list SET intimidation = ? WHERE char_id = ?'''        
    data = (statBlock[5], charID)
    c.execute(sql, data)
    conn.commit()
    
    sql = '''UPDATE char_skill_list SET performance = ? WHERE char_id = ?'''        
    data = (statBlock[5], charID)
    c.execute(sql, data)
    conn.commit()
    
    sql = '''UPDATE char_skill_list SET persuasion = ? WHERE char_id = ?'''        
    data = (statBlock[5], charID)
    c.execute(sql, data)
    conn.commit()
    
def deleteChar(charID):
    # delete character from all tables    
    sql = '''DELETE FROM char_currency WHERE char_id = ?'''
    data = (charID,)
    c.execute(sql, data)
    conn.commit()
    
    sql = '''DELETE FROM char_descriptors WHERE char_id = ?'''
    data = (charID,)
    c.execute(sql, data)
    conn.commit()
    
    sql = '''DELETE FROM char_feats WHERE char_id = ?'''
    data = (charID,)
    c.execute(sql, data)
    conn.commit()
    
    sql = '''DELETE FROM char_inventory WHERE char_id = ?'''
    data = (charID,)
    c.execute(sql, data)
    conn.commit()
    
    sql = '''DELETE FROM char_proficiencies WHERE char_id = ?'''
    data = (charID,)
    c.execute(sql, data)
    conn.commit()
    
    sql = '''DELETE FROM char_saving_throws WHERE char_id = ?'''
    data = (charID,)
    c.execute(sql, data)
    conn.commit()
    
    sql = '''DELETE FROM char_skill_list WHERE char_id = ?'''
    data = (charID,)
    c.execute(sql, data)
    conn.commit()
    
    sql = '''DELETE FROM char_stat_block WHERE char_id = ?'''
    data = (charID,)
    c.execute(sql, data)
    conn.commit()
    
    sql = '''DELETE FROM char_traits WHERE char_id = ?'''
    data = (charID,)
    c.execute(sql, data)
    conn.commit()
    
    sql = '''DELETE FROM user_character_list WHERE char_id = ?'''
    data = (charID,)
    c.execute(sql, data)
    conn.commit()
 
def getProfBonus(lvl):
    if lvl >= 1 and lvl <= 4:
        prof = 2
    elif lvl >= 5 and lvl <= 8:
        prof = 3
    elif lvl >= 9 and lvl <= 12:
        prof = 4
    elif lvl >= 13 and lvl <= 16:
        prof = 5
    elif lvl >= 17 and lvl <= 20:
        prof = 6
         
    return prof

# pass in a list of proficiencies        
def updateProfBonusSkills(profArray, charID):
    # get lvl
    lvl = getLvl(charID)
    
    # get prof bonus
    bonus = getProfBonus(lvl)
    
    profArraySize = len(profArray)
    profIndex = 0
    while(profIndex < profArraySize):
        # compare them to the skills
        if profArray[profIndex] == 'Skill: Athletics':
            # grab current athletics score
            c.execute('SELECT athletics FROM char_skill_list WHERE char_id = ?', [charID])
            data = c.fetchone()
            skill = data[0]
            
            # add prof bonus
            skill += bonus
            
            # insert back into db
            sql = '''UPDATE char_skill_list SET athletics = ? WHERE char_id = ?'''        
            data = (skill, charID)
            c.execute(sql, data)
            conn.commit()
            
        if profArray[profIndex] == 'Skill: Acrobatics':
            # grab current athletics score
            c.execute('SELECT acrobatics FROM char_skill_list WHERE char_id = ?', [charID])
            data = c.fetchone()
            skill = data[0]
            
            # add prof bonus
            skill += bonus
            
            # insert back into db
            sql = '''UPDATE char_skill_list SET acrobatics = ? WHERE char_id = ?'''        
            data = (skill, charID)
            c.execute(sql, data)
            conn.commit()
            
        if profArray[profIndex] == 'Skill: Sleight of Hand':
            # grab current athletics score
            c.execute('SELECT sleight_of_hand FROM char_skill_list WHERE char_id = ?', [charID])
            data = c.fetchone()
            skill = data[0]
            
            # add prof bonus
            skill += bonus
            
            # insert back into db
            sql = '''UPDATE char_skill_list SET sleight_of_hand = ? WHERE char_id = ?'''        
            data = (skill, charID)
            c.execute(sql, data)
            conn.commit()
            
        if profArray[profIndex] == 'Skill: Stealth':
            # grab current athletics score
            c.execute('SELECT stealth FROM char_skill_list WHERE char_id = ?', [charID])
            data = c.fetchone()
            skill = data[0]
            
            # add prof bonus
            skill += bonus
            
            # insert back into db
            sql = '''UPDATE char_skill_list SET stealth = ? WHERE char_id = ?'''        
            data = (skill, charID)
            c.execute(sql, data)
            conn.commit()
            
        if profArray[profIndex] == 'Skill: Arcana': 
            # grab current athletics score
            c.execute('SELECT arcana FROM char_skill_list WHERE char_id = ?', [charID])
            data = c.fetchone()
            skill = data[0]
            
            # add prof bonus
            skill += bonus
            
            # insert back into db
            sql = '''UPDATE char_skill_list SET arcana = ? WHERE char_id = ?'''        
            data = (skill, charID)
            c.execute(sql, data)
            conn.commit()
               
        if profArray[profIndex] == 'Skill: History':
            # grab current athletics score
            c.execute('SELECT history FROM char_skill_list WHERE char_id = ?', [charID])
            data = c.fetchone()
            skill = data[0]
            
            # add prof bonus
            skill += bonus
            
            # insert back into db
            sql = '''UPDATE char_skill_list SET history = ? WHERE char_id = ?'''        
            data = (skill, charID)
            c.execute(sql, data)
            conn.commit()
            
        if profArray[profIndex] == 'Skill: Investigation':
            # grab current athletics score
            c.execute('SELECT investigation FROM char_skill_list WHERE char_id = ?', [charID])
            data = c.fetchone()
            skill = data[0]
            
            # add prof bonus
            skill += bonus
            
            # insert back into db
            sql = '''UPDATE char_skill_list SET investigation = ? WHERE char_id = ?'''        
            data = (skill, charID)
            c.execute(sql, data)
            conn.commit()
            
        if profArray[profIndex] == 'Skill: Nature':
            # grab current athletics score
            c.execute('SELECT nature FROM char_skill_list WHERE char_id = ?', [charID])
            data = c.fetchone()
            skill = data[0]
            
            # add prof bonus
            skill += bonus
            
            # insert back into db
            sql = '''UPDATE char_skill_list SET nature = ? WHERE char_id = ?'''        
            data = (skill, charID)
            c.execute(sql, data)
            conn.commit()
            
        if profArray[profIndex] == 'Skill: Religion':
            # grab current athletics score
            c.execute('SELECT religion FROM char_skill_list WHERE char_id = ?', [charID])
            data = c.fetchone()
            skill = data[0]
            
            # add prof bonus
            skill += bonus
            
            # insert back into db
            sql = '''UPDATE char_skill_list SET religion = ? WHERE char_id = ?'''        
            data = (skill, charID)
            c.execute(sql, data)
            conn.commit()
            
        if profArray[profIndex] == 'Skill: Animal Handling':
            # grab current athletics score
            c.execute('SELECT animal_handling FROM char_skill_list WHERE char_id = ?', [charID])
            data = c.fetchone()
            skill = data[0]
            
            # add prof bonus
            skill += bonus
            
            # insert back into db
            sql = '''UPDATE char_skill_list SET animal_handling = ? WHERE char_id = ?'''        
            data = (skill, charID)
            c.execute(sql, data)
            conn.commit()
            
        if profArray[profIndex] == 'Skill: Insight':    
            # grab current athletics score
            c.execute('SELECT insight FROM char_skill_list WHERE char_id = ?', [charID])
            data = c.fetchone()
            skill = data[0]
            
            # add prof bonus
            skill += bonus
            
            # insert back into db
            sql = '''UPDATE char_skill_list SET insight = ? WHERE char_id = ?'''        
            data = (skill, charID)
            c.execute(sql, data)
            conn.commit()
            
        if profArray[profIndex] == 'Skill: Medicine':
            # grab current athletics score
            c.execute('SELECT medicine FROM char_skill_list WHERE char_id = ?', [charID])
            data = c.fetchone()
            skill = data[0]
            
            # add prof bonus
            skill += bonus
            
            # insert back into db
            sql = '''UPDATE char_skill_list SET medicine = ? WHERE char_id = ?'''        
            data = (skill, charID)
            c.execute(sql, data)
            conn.commit()
            
        if profArray[profIndex] == 'Skill: Perception':
            # grab current athletics score
            c.execute('SELECT perception FROM char_skill_list WHERE char_id = ?', [charID])
            data = c.fetchone()
            skill = data[0]
            
            # add prof bonus
            skill += bonus
            
            # insert back into db
            sql = '''UPDATE char_skill_list SET perception = ? WHERE char_id = ?'''        
            data = (skill, charID)
            c.execute(sql, data)
            conn.commit()
            
        if profArray[profIndex] == 'Skill: Survival':
            # grab current athletics score
            c.execute('SELECT survival FROM char_skill_list WHERE char_id = ?', [charID])
            data = c.fetchone()
            skill = data[0]
            
            # add prof bonus
            skill += bonus
            
            # insert back into db
            sql = '''UPDATE char_skill_list SET survival = ? WHERE char_id = ?'''        
            data = (skill, charID)
            c.execute(sql, data)
            conn.commit()
            
        if profArray[profIndex] == 'Skill: Deception':
            # grab current athletics score
            c.execute('SELECT deception FROM char_skill_list WHERE char_id = ?', [charID])
            data = c.fetchone()
            skill = data[0]
            
            # add prof bonus
            skill += bonus
            
            # insert back into db
            sql = '''UPDATE char_skill_list SET deception = ? WHERE char_id = ?'''        
            data = (skill, charID)
            c.execute(sql, data)
            conn.commit()
            
        if profArray[profIndex] == 'Skill: Intimidation':
            # grab current athletics score
            c.execute('SELECT intimidation FROM char_skill_list WHERE char_id = ?', [charID])
            data = c.fetchone()
            skill = data[0]
            
            # add prof bonus
            skill += bonus
            
            # insert back into db
            sql = '''UPDATE char_skill_list SET intimidation = ? WHERE char_id = ?'''        
            data = (skill, charID)
            c.execute(sql, data)
            conn.commit()
            
        if profArray[profIndex] == 'Skill: Performance':
            # grab current athletics score
            c.execute('SELECT performance FROM char_skill_list WHERE char_id = ?', [charID])
            data = c.fetchone()
            skill = data[0]
            
            # add prof bonus
            skill += bonus
            
            # insert back into db
            sql = '''UPDATE char_skill_list SET performance = ? WHERE char_id = ?'''        
            data = (skill, charID)
            c.execute(sql, data)
            conn.commit()
            
        if profArray[profIndex] == 'Skill: Persuasion':
            # grab current athletics score
            c.execute('SELECT persuasion FROM char_skill_list WHERE char_id = ?', [charID])
            data = c.fetchone()
            skill = data[0]
            
            # add prof bonus
            skill += bonus
            
            # insert back into db
            sql = '''UPDATE char_skill_list SET persuasion = ? WHERE char_id = ?'''        
            data = (skill, charID)
            c.execute(sql, data)
            conn.commit()
    
        # increment 
        profIndex += 1

def updateDescriptors(charID, age, height, weight, eyes, skin, hair, gender, faith):
    # insert back into db
            sql = '''UPDATE char_descriptors SET age = ?, height = ?, weight = ?, eyes = ?, skin = ?, hair = ?, gender = ?, faith = ? WHERE char_id = ?'''        
            data = (age, height, weight, eyes, skin, hair, gender, faith, charID)
            c.execute(sql, data)
            conn.commit()        
        
def updateProfBonusSavingThrows(charID, classID):
    # get lvl
    lvl = getLvl(charID)
    
    # get prof bonus
    bonus = getProfBonus(lvl)
    
    # open class db
    tempConn = sqlite3.connect(CLASS_DB)
    tempC = tempConn.cursor()
    
    # retrieve the saving throw prof
    tempC.execute('SELECT saving_throw_prof FROM saving_throw_prof WHERE class_id = ?', [classID])
    bonusData = tempC.fetchall()
    
    # update the statblock stats
    for row in bonusData:
        if row[0] == 'STR':
            # grab current str saving score
            c.execute('SELECT str_saving FROM char_saving_throws WHERE char_id = ?', [charID])
            data = c.fetchone()
            savingThrow = data[0]
            
            # add prof bonus
            savingThrow += bonus
            
            # insert back into db
            sql = '''UPDATE char_saving_throws SET str_saving = ? WHERE char_id = ?'''        
            data = (savingThrow, charID)
            c.execute(sql, data)
            conn.commit()
            
        elif row[0] == 'DEX':
            # grab current str saving score
            c.execute('SELECT dex_saving FROM char_saving_throws WHERE char_id = ?', [charID])
            data = c.fetchone()
            savingThrow = data[0]
            
            # add prof bonus
            savingThrow += bonus
            
            # insert back into db
            sql = '''UPDATE char_saving_throws SET dex_saving = ? WHERE char_id = ?'''        
            data = (savingThrow, charID)
            c.execute(sql, data)
            conn.commit()
            
        elif row[0] == 'CON':
            # grab current str saving score
            c.execute('SELECT con_saving FROM char_saving_throws WHERE char_id = ?', [charID])
            data = c.fetchone()
            savingThrow = data[0]
            
            # add prof bonus
            savingThrow += bonus
            
            # insert back into db
            sql = '''UPDATE char_saving_throws SET con_saving = ? WHERE char_id = ?'''        
            data = (savingThrow, charID)
            c.execute(sql, data)
            conn.commit()
            
        elif row[0] == 'INT':
            # grab current str saving score
            c.execute('SELECT int_saving FROM char_saving_throws WHERE char_id = ?', [charID])
            data = c.fetchone()
            savingThrow = data[0]
            
            # add prof bonus
            savingThrow += bonus
            
            # insert back into db
            sql = '''UPDATE char_saving_throws SET int_saving = ? WHERE char_id = ?'''        
            data = (savingThrow, charID)
            c.execute(sql, data)
            conn.commit()
            
        elif row[0] == 'WIS':
            # grab current str saving score
            c.execute('SELECT wis_saving FROM char_saving_throws WHERE char_id = ?', [charID])
            data = c.fetchone()
            savingThrow = data[0]
            
            # add prof bonus
            savingThrow += bonus
            
            # insert back into db
            sql = '''UPDATE char_saving_throws SET wis_saving = ? WHERE char_id = ?'''        
            data = (savingThrow, charID)
            c.execute(sql, data)
            conn.commit()
            
        elif row[0] == 'CHA':
            # grab current str saving score
            c.execute('SELECT cha_saving FROM char_saving_throws WHERE char_id = ?', [charID])
            data = c.fetchone()
            savingThrow = data[0]
            
            # add prof bonus
            savingThrow += bonus
            
            # insert back into db
            sql = '''UPDATE char_saving_throws SET cha_saving = ? WHERE char_id = ?'''        
            data = (savingThrow, charID)
            c.execute(sql, data)
            conn.commit()
        else:
            print("error - unkown type") 
    
    # close out our cursor 
    tempC.close()
    tempConn.close()