# Author:  Manuel Perez
# Date:    09/13/2020
# Purpose: Pull spell data from an api and create
# a DB
#
####################################################
# import some libraries for api things and sqlite3
import requests
import sqlite3

# open a connection to our db and create a cursor
conn = sqlite3.connect('DnDCompanion_Spells.db')
c = conn.cursor();

# opening the api and creating a json obj
resp = requests.get('https://www.dnd5eapi.co/api/spells/')
json_obj = resp.json()

# =========================================================================
# my functions
def createTables():
    # creates table spells
    c.execute('''CREATE TABLE IF NOT EXISTS spells (
        spell_id integer PRIMARY KEY,
        spell_name text, spell_desc text, higher_levels text,
        spell_range text,spell_components text, spell_materials text,
        ritual text, spell_duration text, concentration text,
        casting_time text, spell_level integer, spell_school text)''')
    
    # create table schools_of_magic
    c.execute('''CREATE TABLE IF NOT EXISTS schools_of_magic (
        school_id integer PRIMARY KEY,
        school_name text)''')
    
    # create table classes_spell_list
    c.execute('''CREATE TABLE IF NOT EXISTS classes_spell_list (
        spell_id integer, classes text)''')
    
    # create table damage_spells
    c.execute('''CREATE TABLE IF NOT EXISTS damage_spells (
    spell_id integer, attack_type text, damage_type text,
    damage_at_slot_level text, dc_type text,
    dc_success text)''')
    
    # create table dmg_types
    c.execute('''CREATE TABLE IF NOT EXISTS dmg_types (
        dmg_type_id integer PRIMARY KEY, dmg_type text)''')
    
    # create table healing spells table
    c.execute('''CREATE TABLE IF NOT EXISTS healing_spells (
        spell_id integer PRIMARY KEY,
        heal_at_slot_level text)''')
    
def insertSchools():
    # create a list of the schools
    schoolList = ['Abjuration', 'Conjuration', 'Divination',
                   'Enchantment', 'Illusion', 'Necromancy', 
                   'Transmutation']
    schoolListIndex = 1
    for rows in schoolList:
        schools = [schoolListIndex, rows]
        sql = 'INSERT INTO schools_of_magic VALUES(?,?)'
        c.execute(sql, schools)
        schoolListIndex += 1
        
        # commit these changes
        conn.commit()

def insertDmgType():
    # create a list of dmg_types
    dmgTypeList = ['Acid', 'Bludgeoning', 'Cold',
                   'Fire', 'Force', 'Lightning', 
                   'Necrotic', 'Piercing', 'Poison', 
                   'Psychic', 'Radiant', 'Slashing', 
                   'Thunder']
    dmgTypeListIndex = 1
    for rows in dmgTypeList:
        dmgType = [dmgTypeListIndex, rows]
        sql = 'INSERT INTO dmg_types VALUES(?,?)'
        c.execute(sql, dmgType)
        dmgTypeListIndex += 1
        
        # commit these changes
        conn.commit()
        
def dropTables():
    c.execute('DROP TABLE spells')
    c.execute('DROP TABLE schools_of_magic')
    c.execute('DROP TABLE classes_spell_list')
    c.execute('DROP TABLE damage_spells')
    c.execute('DROP TABLE dmg_types')
    c.execute('DROP TABLE healing_spells')
    
def spellSearch(query):
    url = 'https://www.dnd5eapi.co' + query
    return url

def dataEntry(json_obj2):
    global count
    
    # Obtain all the data for spells table
    spellName = json_obj2['name']
    spellDesc = str(json_obj2['desc'])
    if 'higher_level' in json_obj2:
        higherLevels = str(json_obj2['higher_level'])
    else:
        higherLevels = 'n/a'
    spellRange = json_obj2['range']
    spellComponents = str(json_obj2['components'])
    if 'material' in json_obj2:
        spellMaterial = json_obj2['material']
    else:
        spellMaterial = 'n/a'   
    ritual = str(json_obj2['ritual'])
    spellDuration = json_obj2['duration']
    concentration = str(json_obj2['concentration'])
    castingTime = json_obj2['casting_time']
    spellLevel = json_obj2['level']
    spellSchool = str(json_obj2['school']['name'])
    
    # create a list of spell values
    spells = [count, spellName, spellDesc, higherLevels,
        spellRange, spellComponents, spellMaterial,
        ritual, spellDuration, concentration,
        castingTime, spellLevel, spellSchool]
    
    # insert list into spells table
    sql = 'INSERT INTO spells VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)'
    c.execute(sql, spells)
    
# =========================================================================
    # update the table classes_spell_list users
    sql = 'INSERT INTO classes_spell_list VALUES (?,?)'
    for rows in json_obj2['classes']:
        classes = rows['name']
        classesList = [count, classes]
        c.execute(sql, classesList)

# =========================================================================
    #update the table dmg_spells
    if 'attack_type' in json_obj2:
        attackType = json_obj2['attack_type']
    else:
        attackType = 'n/a'
    
    if 'damage' in json_obj2:
        # check if damage type exists
        if 'damage_type' in json_obj2['damage']:
            damageType = str(json_obj2['damage']['damage_type']['name'])
        else:
            damageType = 'n/a'
            
        # check if damage at slot exists
        if 'damage_at_slot_level' in json_obj2['damage']:        
            damageAsYouLevel = str(json_obj2['damage']['damage_at_slot_level'])
        elif 'damage_at_character_level' in json_obj2['damage']:
            damageAsYouLevel = str(json_obj2['damage']['damage_at_character_level'])
        else:
            damageAsYouLevel = 'n/a'
            
        # check if dc exists
        if 'dc' in json_obj2:
            dc_type = json_obj2['dc']['dc_type']['name']
            dc_success = json_obj2['dc']['dc_success']
        else:
            dc_type = 'n/a'
            dc_success = 'n/a'
            
        # insert list into damage_spells table 
        damageSpellList = [count, attackType, damageType, 
                           damageAsYouLevel, dc_type, dc_success]
        sql = 'INSERT INTO damage_spells VALUES (?,?,?,?,?,?)'
        c.execute(sql, damageSpellList)
        
# =========================================================================    
    # check if healing spell
    if 'heal_at_slot_level' in json_obj2:
        healingSpellsPerLvl = str(json_obj2['heal_at_slot_level'])
        healingSpells = [count, healingSpellsPerLvl]
        sql = 'INSERT INTO healing_spells VALUES (?,?)'
        c.execute(sql, healingSpells)

    # commit these changes
    conn.commit()
    print('Complete ' + str(count) + '/319')
    count += 1
    
# =========================================================================
# create the table if it doesn't exist
createTables()
insertSchools()
insertDmgType()
count = 1

# interate through all the spells urls
for spellIndex in json_obj['results']:
    # returns the spell url and places it in a json obj
    resp2 = requests.get(spellSearch(spellIndex['url']))
    json_obj2 = resp2.json()
    
    # insert data into table
    dataEntry(json_obj2)
    
# close out our cursor 
c.close()
conn.close()
