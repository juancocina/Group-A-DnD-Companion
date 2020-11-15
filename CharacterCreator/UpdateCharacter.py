# Author:  Manuel Perez
# Date:    10/05/2020
# Purpose: This is our character creator
#
####################################################################
# import some libraries
import sqlite3

# open a connection to our db and create a cursor
conn = sqlite3.connect('DnDEZ_CharacterList.db')
c = conn.cursor();

# Functions ########################################################
# create default char
def createDefaultChar(newUserID, newCharID):
    # set ID's
    userID = newUserID 
    charID = newCharID
    
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
    
    newCharList = [userID, charID, charName,
                   charLvl, raceID, classID,
                   backgroundID, alignment, profBonus,
                   AC, initiative, speed, max_hp,
                   hit_die_type, num_hit_die]

    # insert into char list table
    sql = '''INSERT INTO characters VALUES 
    (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)'''
    c.execute(sql, newCharList)
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
    
def getRaceID(raceName):
    # open race db
    tempConn = sqlite3.connect('DnDEZ_Race.db')
    tempC = tempConn.cursor()
    
    # retrieve the race_id by using race_name
    tempC.execute('SELECT race_id FROM race WHERE race_name = ?', [raceName])
    data = tempC.fetchone()
    
    # close race db
    tempC.close()
    tempConn.close()
    
    return data[0]

def getClassID(className):
    # open class db
    tempConn = sqlite3.connect('DnDEZ_Class.db')
    tempC = tempConn.cursor()
    
    # retrieve the race_id by using race_name
    tempC.execute('SELECT class_id FROM class WHERE class_name = ?', [className])
    data = tempC.fetchone()
    
    # close race db
    tempC.close()
    tempConn.close()
    
    return data[0]

def getSpeed(raceID): 
    # open race db
    tempConn = sqlite3.connect('DnDEZ_Race.db')
    tempC = tempConn.cursor()
    
    # retrieve the race_id by using race_name
    tempC.execute('SELECT speed FROM race WHERE race_id = ?', [raceID])
    data = tempC.fetchone()
    
    # close race db
    tempC.close()
    tempConn.close()
    
    return data[0]

def getLangKnown(raceID):
    # open race db
    tempConn = sqlite3.connect('DnDEZ_Race.db')
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
    tempConn = sqlite3.connect('DnDEZ_Race.db')
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
    tempConn = sqlite3.connect('DnDEZ_Class.db')
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
    tempConn = sqlite3.connect('DnDEZ_Class.db')
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
    sql = '''UPDATE characters SET char_name = ? WHERE char_id = ?'''        
    data = (charName, charID)
    c.execute(sql, data)
    conn.commit()
    
def updateCharLvl(charID, lvl):
    # update char lvl
    sql = '''UPDATE characters SET char_lvl = ? WHERE char_id = ?'''        
    data = (lvl, charID)
    c.execute(sql, data)
    conn.commit()
    
    # update num of hit die
    sql = '''UPDATE characters SET num_hit_die = ? WHERE char_id = ?'''        
    data = (lvl, charID)
    c.execute(sql, data)
    conn.commit()

def updateBackground(charID, background):
    # update background
    sql = '''UPDATE characters SET background_id = ? WHERE char_id = ?'''        
    data = (background, charID)
    c.execute(sql, data)
    conn.commit()
    
def updateAlignment(charID, alignment):
    # update alignment
    sql = '''UPDATE characters SET alignment = ? WHERE char_id = ?'''        
    data = (alignment, charID)
    c.execute(sql, data)
    conn.commit()

def updateProfBonus(charID, profBon):
    # update prof bon
    sql = '''UPDATE characters SET prof_bonus = ? WHERE char_id = ?'''        
    data = (profBon, charID)
    c.execute(sql, data)
    conn.commit()

def updateAC(charID, ac):
    # update prof bon
    sql = '''UPDATE characters SET AC = ? WHERE char_id = ?'''        
    data = (ac, charID)
    c.execute(sql, data)
    conn.commit()

def updateInitiative(charID, initiative):
    # update initiative
    sql = '''UPDATE characters SET initiative = ? WHERE char_id = ?'''        
    data = (initiative, charID)
    c.execute(sql, data)
    conn.commit()

def updateHP(charID, hp):
    # update hp
    sql = '''UPDATE characters SET max_hp = ? WHERE char_id = ?'''        
    data = (hp, charID)
    c.execute(sql, data)
    conn.commit()
    
def updateRace(raceName, charID):
    # update race_id
    raceID = getRaceID(raceName)
    sql = '''UPDATE characters SET race_id = ? WHERE char_id = ?'''        
    data = (raceID, charID)
    c.execute(sql, data)
    conn.commit()
    
    # update speed
    speed = getSpeed(raceID)
    sql = '''UPDATE characters SET speed = ? WHERE char_id = ?'''        
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
    
    
def updateClass(className, charID, raceID):
    # update class_id
    classID = getClassID(className)
    sql = '''UPDATE characters SET class_id = ? WHERE char_id = ?'''        
    data = (classID, charID)
    c.execute(sql, data)
    conn.commit()
    
    # update hit die type
    hitDie = getHitDieType(classID)
    sql = '''UPDATE characters SET hit_die_type = ? WHERE char_id = ?'''        
    data = (hitDie, charID)
    c.execute(sql, data)
    conn.commit()

    # I need to figure out how to categorize them
    # update starting prof
#    profList = getStartingProf(raceID, classID)
#    sql = '''UPDATE char_proficiencies SET languages = ? WHERE char_id = ?'''        
#    data = (str(profList), charID)
#    c.execute(sql, data)
#    conn.commit()

# update stat block
def updateStatBlock(charID, raceID, statBlock):
    # open race db
    tempConn = sqlite3.connect('DnDEZ_Race.db')
    tempC = tempConn.cursor()
    
    # retrieve the bonus type and unit using race_id
    tempC.execute('SELECT stat_name, bonus FROM stat_bonuses WHERE race_id = ?', [raceID])
    bonusData = tempC.fetchall()
    
    # update the statblock stats
    for row in bonusData:
        if row[0] == 'STR':
            statBlock[0] += row[1]
        elif row[0] == 'DEX':
            statBlock[1] += row[1]
        elif row[0] == 'CON':
            statBlock[2] += row[1]
        elif row[0] == 'INT':
            statBlock[3] += row[1]
        elif row[0] == 'WIS':
            statBlock[4] += row[1]
        elif row[0] == 'CHA':
            statBlock[5] += row[1]
        else:
            print("error - unkown type") 
    
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
    convertStatsToMods(statBlock)
    updateSkills(charID, statBlock)
    updateSavingThrows(charID, statBlock)
    
def convertStatsToMods(statBlock):
    sbIndex = 0
    
    for index in statBlock:
        if index == 1:
            statBlock[sbIndex] = -5
        elif index == 2 or index == 3:
            statBlock[sbIndex] = -4
        elif index == 4 or index == 5:
            statBlock[sbIndex] = -3
        elif index == 6 or index == 7:
            statBlock[sbIndex] = -2
        elif index == 8 or index == 9:
            statBlock[sbIndex] = -1
        elif index == 10 or index == 11:
            statBlock[sbIndex] = 0
        elif index == 12 or index == 13:
            statBlock[sbIndex] = 1
        elif index == 14 or index == 15:
            statBlock[sbIndex] = 2
        elif index == 16 or index == 17:
            statBlock[sbIndex] = 3
        elif index == 18 or index == 19:
            statBlock[sbIndex] = 4 
        elif index >= 20:
            statBlock[sbIndex] = 5
        
        sbIndex += 1

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
    
    sql = '''DELETE FROM characters WHERE char_id = ?'''
    data = (charID,)
    c.execute(sql, data)
    conn.commit()
    
####################################################################
# MAIN
#deleteChar('CH0001')
#createDefaultChar('US0001', 'CH0001')
#updateRace('Human', 'CH0001')
#updateClass('Barbarian', 'CH0001')
#updateStatBlock('CH0001', 'RA8', [1,3,7,13,15,20])
#getStartingProf('RA2','CL1')
updateName('CH0001', 'Ulrich Bronzebeard')