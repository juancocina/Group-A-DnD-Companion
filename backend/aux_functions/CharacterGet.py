# Author:  Manuel Perez
# Date:    10/05/2020
# Purpose: This is our character creator
#
####################################################################
# import some libraries
import sqlite3

# Static DB path globals
CHARACTER_DB = '../database/db/DnDEZ_Character.db'
CLASS_DB = '../database/db/DnDEZ_Class.db'
RACE_DB = '../database/db/DnDEZ_Race.db'


# open a connection to our db and create a cursor
conn = sqlite3.connect(CHARACTER_DB, check_same_thread=False)
c = conn.cursor()

# Functions ########################################################

def getSavings(charID):
    # get saving throws
    c.execute('SELECT * FROM char_saving_throws WHERE char_id = ?', [charID])
    data = c.fetchone()
    return data
  
def getSkills(charID):
    # get skills
    c.execute('SELECT * FROM char_skill_list WHERE char_id = ?', [charID])
    data = c.fetchone()
    return data
    
def getCurrency(charID):
    # get skills
    c.execute('SELECT * FROM char_currency WHERE char_id = ?', [charID])
    data = c.fetchone()
    return data

def getDescriptors(charID):
    # get skills
    c.execute('SELECT * FROM char_descriptors WHERE char_id = ?', [charID])
    data = c.fetchone()
    return data
    
def getFeats(charID):
    # get skills
    c.execute('SELECT * FROM char_feats WHERE char_id = ?', [charID])
    data = c.fetchone()
    return data

def getInventory(charID):
    # get skills
    c.execute('SELECT * FROM char_inventory WHERE char_id = ?', [charID])
    data = c.fetchone()
    return data

def getProficiencies(charID):
    # get skills
    c.execute('SELECT * FROM char_proficiencies WHERE char_id = ?', [charID])
    data = c.fetchone()
    return data

def getStatBlock(charID):
    # get skills
    c.execute('SELECT * FROM char_stat_block WHERE char_id = ?', [charID])
    data = c.fetchone()
    return data

def getTraits(charID):
    # get skills
    c.execute('SELECT * FROM char_traits WHERE char_id = ?', [charID])
    data = c.fetchone()
    return data
    
def getCharacter(charID):
    # get skills
    c.execute('SELECT * FROM user_character_list WHERE char_id = ?', [charID])
    data = c.fetchone()
    return data
    
    # close out our cursor 
    tempC.close()
    tempConn.close()