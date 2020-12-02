# Author: Joshua Nathan
# For cpsc 362 DND Ez project 

# This file contains database queries to get character and campaign information associated with a specific account

import sqlite3

# Static DB path globals
CHARACTER_DB = '../database/db/DnDEZ_Character.db'
CLASS_DB = '../database/db/DnDEZ_Class.db'
RACE_DB = '../database/db/DnDEZ_Race.db'
CAMPAIGN_DATABASE = '../database/db/DnDEZ_Campaigns.db'



def query_account_characters(user_id):
    conn = sqlite3.connect(CHARACTER_DB)
    c = conn.cursor()
    c.execute("SELECT char_id, char_name, char_lvl, race_id, class_id FROM user_character_list WHERE user_id=?", (user_id,))
    data = c.fetchall()
    c.close()
    conn.close()

    conn = sqlite3.connect(RACE_DB)
    c = conn.cursor()
    temp = []
    for item in data:
        c.execute("SELECT race_name FROM race WHERE race_id=?",(item[3],))
        race_name = c.fetchall()[0][0]
        val = list(item)
        val[-2] = race_name
        temp.append(tuple(val))
    c.close()
    conn.close()

    conn = sqlite3.connect(CLASS_DB)
    c = conn.cursor()

    temp2 = []
    for item in temp:
        c.execute("SELECT class_name FROM class WHERE class_id=?", (item[4],))
        class_name = c.fetchall()[0][0]
        val = list(item)
        val[-1] = class_name
        temp2.append(tuple(val))

    c.close()
    conn.close()

    return temp2

def query_account_campaigns(user_id):
    conn = sqlite3.connect(CAMPAIGN_DATABASE)
    c = conn.cursor()
    c.execute("SELECT campaign_name, campaign_description, date_created, campaign_id, thumbnail_path FROM campaigns WHERE user_id=?", (user_id,))
    data = c.fetchall()
    c.close()
    conn.close()

    return data

def delete_account_campaign(campaign_id):
    conn = sqlite3.connect(CAMPAIGN_DATABASE)
    c = conn.cursor()
    c.execute("DELETE FROM campaigns WHERE campaign_id=?", (campaign_id,))
    c.execute("DELETE FROM maps WHERE campaign_id=?", (campaign_id,))
    conn.commit()
    c.close()
    conn.close()


def query_campaign(campaign_id):
    conn = sqlite3.connect(CAMPAIGN_DATABASE)
    c=conn.cursor()
    c.execute("SELECT date_created, campaign_name, campaign_description, thumbnail_path FROM campaigns WHERE campaign_id=?", (campaign_id,))
    c_data = c.fetchall()
    c.execute("SELECT map_id, map_name, map_description, map_path FROM maps WHERE campaign_id=?", (campaign_id,))
    m_data = c.fetchall()

    return c_data, m_data