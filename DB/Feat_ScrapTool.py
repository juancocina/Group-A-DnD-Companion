# Author:  Manuel Perez
# Date:    09/13/2020
# Purpose: Pull feat data from an api and create
# a DB
#
####################################################
# import some libraries for api things and sqlite3
import requests
import sqlite3

# open a connection to our db and create a cursor
conn = sqlite3.connect('DnDCompanion_Feats.db')
c = conn.cursor();

# opening the api and creating a json obj
resp = requests.get('https://www.dnd5eapi.co/api/features/')
json_obj = resp.json()

# =========================================================================
# my functions
def createTable():
    # creates table spells
    c.execute('''CREATE TABLE IF NOT EXISTS feats (
        feat_id integer PRIMARY KEY, feat_class text, 
        feat_name text, feat_level integer,
        feat_desc text, pre_req_type text, pre_req text,
        grouping text, subclass text, num_you_choose integer,
        list_of_choices text)''')
        
def dropTables():
    c.execute('DROP TABLE feats')
    
def featSearch(query):
    url = 'https://www.dnd5eapi.co' + query
    return url
    
def dataEntry(json_obj):  
    global count
      
    # Obtain all the data for feat table
    featClass = json_obj['class']['name']
    featName = json_obj['name']
    if 'level' in json_obj:
        featLevel = json_obj['level']
    else:
        featLevel = 'n/a'
        
    desc = json_obj['desc']
    desc = str(desc)
    
    # there are some empty lists in prereqs
    if 'prerequisites' in json_obj and len(json_obj['prerequisites']) != 0:
        preReqType = json_obj['prerequisites'][0]['type']
        if preReqType == 'level':
            preReq = json_obj['prerequisites'][0]['level']
        elif preReqType == 'Spell':
            # if spell get the spell name
            spellURL = featSearch(json_obj['prerequisites'][0]['spell'])
            resp = requests.get(spellURL)
            temp_obj = resp.json()
            temp_obj
            preReq = temp_obj['name']
        elif preReqType == 'feature':
            # if feat get the feat name
            featURL = featSearch(json_obj['prerequisites'][0]['feature'])
            resp = requests.get(featURL)
            temp_obj = resp.json()
            temp_obj
            preReq = temp_obj['name']
        elif preReqType == 'proficiency':
            # if prof get the prof name
            profURL = featSearch(json_obj['prerequisites'][0]['proficiency'])
            resp = requests.get(profURL)
            temp_obj = resp.json()
            temp_obj
            preReq = temp_obj['name']
        else:
            preReq = 'n/a'
            preReqType = 'n/a'            
    else:    
        preReq = 'n/a'
        preReqType = 'n/a'
        
    if 'group' in json_obj:
        group = json_obj['group']
    else:
        group = 'n/a'
        
    if 'subclass' in json_obj:
        subclass = json_obj['subclass']['name']
    else:
        subclass = 'n/a'
        
    if 'choice' in json_obj:
        # number you choose
        numYouChoose = json_obj['choice']['choose']
        
        # make a list of all the choices
        listOfChoices = []
        for numOfChoices in json_obj['choice']['from']:    
            listOfChoices.append(numOfChoices['name'])
            
        listOfChoices = str(listOfChoices)
            
    else:
        numYouChoose = 'n/a'
        listOfChoices = 'n/a'
    
    # insert list into damage_spells table 
    featTableList = [count, featClass, featName, 
                        featLevel, desc, preReqType,
                        preReq, group, subclass,
                        numYouChoose, listOfChoices]
    sql = 'INSERT INTO feats VALUES (?,?,?,?,?,?,?,?,?,?,?)'
    c.execute(sql, featTableList)        
# =========================================================================    

    # commit these changes
    conn.commit()
    print('Complete ' + str(count) + '/414')
    count += 1
    
# =========================================================================
# create the table if it doesn't exist
dropTables()
createTable()
count = 1

# interate through all the spells urls
for featIndex in json_obj['results']:
    # returns the spell url and places it in a json obj
    resp2 = requests.get(featSearch(featIndex['url']))
    json_obj2 = resp2.json()
    
    # insert data into table
    dataEntry(json_obj2)
    
# close out our cursor 
c.close()
conn.close()