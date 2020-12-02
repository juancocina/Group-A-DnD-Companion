# Author:  Manuel Perez
# Date:    10/18/2020
# Purpose: Create Character DB
#
####################################################
# import some libraries for api things and sqlite3
import sqlite3

# open a connection to our db and create a cursor
conn = sqlite3.connect('DnDEZ_Character.db')
c = conn.cursor();

# =========================================================================
# my functions
def createTables():
    # creates table characters
    c.execute('''CREATE TABLE IF NOT EXISTS characters (
        user_id text, char_id text PRIMARY KEY, char_name text,
        char_lvl int, race_id text, class_id text,
        background_id text, alignment text, prof_bonus int,
        AC int, initiative int, speed int, max_hp int,
        hit_die_type text, num_hit_die int)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS char_descriptors (
        char_id text, age text, height text,
        weight text, eyes text, skin text, 
        hair text)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS char_proficiencies (
    char_id text, armor_prof text, weapon_prof text,
    shield_prof text, tool_prof text, languages text)''')

    c.execute('''CREATE TABLE IF NOT EXISTS char_feats (
    char_id text, feat_id text)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS char_traits (
    char_id text, personality_traits text, bonds text,
    flaws text)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS char_stat_block (
    char_id text, strength int, dexterity int,
    constitution int, intelligence int, wisdom int,
    charisma int)''')
 
    c.execute('''CREATE TABLE IF NOT EXISTS char_skill_list (
    char_id text, acrobatics int, animal_handling int,
    arcana int, athletics int, deception int,
    history int, insight int, intimidation int,
    investigation int, medicine int, nature int,
    perception int, performance int, persuasion int,
    religion int, sleight_of_hand int, stealth int, 
    survival int)''')
 
    c.execute('''CREATE TABLE IF NOT EXISTS char_saving_throws (
    char_id text, str_saving int, dex_saving int,
    con_saving int, int_saving int, wis_saving int,
    cha_saving int)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS char_inventory (
    char_id text, item_id text, item_quantity int)''')
 
    c.execute('''CREATE TABLE IF NOT EXISTS char_currency (
    char_id text, cp int, sp int, ep int, gp int, pp int)''')
    
def dropTables():
    c.execute('DROP TABLE characters')
    c.execute('DROP TABLE char_descriptors')
    c.execute('DROP TABLE char_proficiencies')
    c.execute('DROP TABLE char_feats')
    c.execute('DROP TABLE char_traits')
    c.execute('DROP TABLE char_stat_block')
    c.execute('DROP TABLE char_skill_list')
    c.execute('DROP TABLE char_saving_throws')
    c.execute('DROP TABLE char_inventory')
    c.execute('DROP TABLE char_currency')

###################################################################
# MAIN 
createTables()





