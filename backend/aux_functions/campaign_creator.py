import sqlite3
import datetime
from datetime import date
from PIL import Image

CAMPAIGN_DATABASE = '../database/db/DnDEZ_Campaigns.db'





def create_new_campaign(user_id,name,description):
    today = date.today()
    format_date = today.strftime("%m/%d/%y")
    conn = sqlite3.connect(CAMPAIGN_DATABASE)
    c = conn.cursor()
    c.execute("INSERT INTO campaigns (user_id, date_created, campaign_name, campaign_description) VALUES (?,?,?,?)", (user_id, format_date, name, description))
    conn.commit()
    c.execute("SELECT last_insert_rowid()")
    c_id = c.fetchall()[0][0]

    return c_id

def update_campaign_cover(campaign_id, img_name):
    conn = sqlite3.connect(CAMPAIGN_DATABASE)
    c = conn.cursor()
    c.execute("UPDATE campaigns SET thumbnail_path=? WHERE campaign_id=?", (img_name, campaign_id))
    conn.commit()
    c.close()
    conn.close()
