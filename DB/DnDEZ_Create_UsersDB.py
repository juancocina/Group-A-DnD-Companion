# Author:  Manuel Perez
# Date:    10/18/2020
# Purpose: Create Character DB
#
####################################################
# import some libraries for api things and sqlite3
import sqlite3

# open a connection to our db and create a cursor
conn = sqlite3.connect('DnDEZ_Users.db')
c = conn.cursor();

# =========================================================================
# my functions
def createTables():
    # creates table characters
    c.execute('''CREATE TABLE IF NOT EXISTS users (
        user_id text PRIMARY KEY, email text NOT NULL UNIQUE, 
        username text NOT NULL UNIQUE, password text NOT NULL)''')

def dropTables():
    c.execute('DROP TABLE users')


###################################################################
# MAIN 
createTables()







