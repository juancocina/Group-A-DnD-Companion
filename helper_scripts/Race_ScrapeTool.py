# Author:  Manuel Perez
# Date:    10/08/2020
# Purpose: Pull the race data from the API
#
####################################################
# import some libraries for api things and sqlite3
import requests
import sqlite3

# open a connection to our db and create a cursor
conn = sqlite3.connect('DnDCompanion_Race.db')
c = conn.cursor();

# opening the api and creating a json obj
raceResp = requests.get('https://www.dnd5eapi.co/api/races/')
json_obj = raceResp.json()


# global counts
count = 1

# =========================================================================
# my functions
def createTables():
    # creates table races
    c.execute('''CREATE TABLE IF NOT EXISTS race (
        race_id text PRIMARY KEY, race_name text, speed int, 
        alignment text, age text, size text, size_desc text, 
        lang_desc text)''')
    c.execute('''CREATE TABLE IF NOT EXISTS traits_known (
        race_id text, trait_id text)''')
    c.execute('''CREATE TABLE IF NOT EXISTS traits_choose_from (
        race_id text, pick_num_traits int, trait_option_id text)''')
    c.execute('''CREATE TABLE IF NOT EXISTS starting_prof (
        race_id text, proficiency text)''')
    c.execute('''CREATE TABLE IF NOT EXISTS stat_bonuses (
        race_id text, stat_name text, bonus int)''')
    c.execute('''CREATE TABLE IF NOT EXISTS languages (
        lang_id text PRIMARY KEY, lang text)''')
    c.execute('''CREATE TABLE IF NOT EXISTS languages_known (
        race_id text, lang_id text)''')
    c.execute('''CREATE TABLE IF NOT EXISTS lang_choose_from (
        race_id text, pick_num_lang int, lang_option_id text)''')

def dropTables():
    c.execute('DROP TABLE race')
    c.execute('DROP TABLE traits_known')
    c.execute('DROP TABLE traits_choose_from')
    c.execute('DROP TABLE starting_prof')
    c.execute('DROP TABLE stat_bonuses')
    c.execute('DROP TABLE languages')
    c.execute('DROP TABLE languages_known')
    c.execute('DROP TABLE lang_choose_from')
    
def insertIntoTable(sqlString, tableList):
    c.execute(sqlString, tableList)
    
def dataURL(query):
    url = 'https://www.dnd5eapi.co' + query
    return url

def createConnection(db_file):
    conn = None
    conn = sqlite3.connect(db_file)
    return conn

def fillLanguageTable():
    langCount = 0
    maxLangs = 16
    langList = ['Common', 'Dwarvish', 'Elvish', 
                'Giant', 'Gnomish', 'Goblin', 
                'Halfling', 'Orcish', 'Abyssal',
                'Celestial', 'Draconic', 'Deep Speech',
                'Infernal', 'Primordial', 'Sylvan',
                'Undercommon']
    while langCount < maxLangs:
        langID = 'LANG' + str(langCount)
        langTableList = [langID, langList[langCount]]
        langCount += 1
        insertIntoTable('INSERT INTO languages VALUES (?,?)', langTableList)
        print('Complete ' + str(langCount) + '/16')
        
def dataEntry(json_obj):  
    global count
    
    # obtain race info
    raceID = 'RA' + str(count)
    raceName = json_obj['name']
    speed = json_obj['speed']
    raceAlignment = json_obj['alignment']
    age = json_obj['age']
    raceSize = json_obj['size']
    sizeDesc = json_obj['size_description']
    languageDesc = json_obj['language_desc']

    # insert into race table
    raceList = [raceID, raceName, speed, raceAlignment,
                age, raceSize, sizeDesc, languageDesc]
    sql = 'INSERT INTO race VALUES (?,?,?,?,?,?,?,?)'
    insertIntoTable(sql, raceList)
    
    # get the ability score bonuses
    for abilScoreBonusIndex in json_obj['ability_bonuses']:
        bonusName = abilScoreBonusIndex['name']
        bonus = abilScoreBonusIndex['bonus']
        
        # insert into stat bonuses
        abilScoreBonList = [raceID, bonusName, bonus]
        insertIntoTable('INSERT INTO stat_bonuses VALUES (?,?,?)', abilScoreBonList)
        
    
    # COME BACK WHEN YOU FINISH THE PROF DB AND FIX ####################################
    # get all the starting proficiencies 
    for profIndex in json_obj['starting_proficiencies']:
        prof = profIndex['name']
        
        # insert into starting prof table
        startPofList = [raceID, prof]
        insertIntoTable('INSERT INTO starting_prof VALUES (?,?)', startPofList)
          
    # get all the starting languages
    for langIndex in json_obj['languages']:
        # retrieve the lang id using the lang name
        c.execute('SELECT lang_id FROM languages WHERE lang = ?', (langIndex['name'],))
        fetchedLangID = c.fetchone()
    
        # insert into languages known table
        langKnownList = [raceID, fetchedLangID[0]]
        insertIntoTable('INSERT INTO languages_known VALUES (?,?)', langKnownList)
        
    # if you have to choose from a list
    if 'language_options' in json_obj:
        langOptNumChoices = json_obj['language_options']['choose']
        
        for langChooseFromIndex in json_obj['language_options']['from']:
            # retrieve the lang id using the lang name
            c.execute('SELECT lang_id FROM languages WHERE lang = ?', (langChooseFromIndex['name'],))
            fetchedLangID = c.fetchone()
           
            # there is an error when dealing with orc so if orc shows up asign orcish id
            if langChooseFromIndex['name'] == 'Orc':
                fetchedLangID = ['LANG7']
                
            # insert into lang option table
            langOptionList = [raceID, langOptNumChoices, fetchedLangID[0]]
            insertIntoTable('INSERT INTO lang_choose_from VALUES (?,?,?)', langOptionList)
    
    # COME BACK WHEN YOU FINISH THE TRAITS DB AND FIX ######################################
    for traitIndex in json_obj['traits']:
        trait = traitIndex['name']
    
        # insert into trait known table
        traitList = [raceID, trait]
        insertIntoTable('INSERT INTO traits_known VALUES (?,?)', traitList)
    
    if 'trait_options' in json_obj:
        traitNumChoices = json_obj['trait_options']['choose']
      
        for traitChooseFrom in json_obj['trait_options']['from']:
            traitOption = traitChooseFrom['name']
            
            # insert into trait choose from table
            traitChoiceList = [raceID, traitNumChoices, traitOption]
            insertIntoTable('INSERT INTO traits_choose_from VALUES (?,?,?)', traitChoiceList)
  
# =========================================================================    
    # commit these changes
    conn.commit()
    print('Complete ' + str(count) + '/9')
    count += 1
    
# =========================================================================
# create the table if it doesn't exist
dropTables()
createTables()

# fill the language table
fillLanguageTable()

# iterate through all the race urls
for raceIndex in json_obj['results']:
    # returns the item url and places it in a json obj
    resp2 = requests.get(dataURL(raceIndex['url']))
    json_obj2 = resp2.json()
    
    # insert data into table
    dataEntry(json_obj2)
    
# close out our cursor 
c.close()
conn.close()