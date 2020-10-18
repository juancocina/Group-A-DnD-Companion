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
conn = sqlite3.connect('DnDCompanion_Items.db')
c = conn.cursor();

# opening the api and creating a json obj
equipResp = requests.get('https://www.dnd5eapi.co/api/equipment/')
weaponPropResp = requests.get('https://www.dnd5eapi.co/api/weapon-properties/')
json_obj = equipResp.json()
json_obj3 = weaponPropResp.json()

# global counts
count = 1
vehicleCount = 1
armorCount = 1
weaponCount = 1
weaponPropCount = 1

# =========================================================================
# my functions
def createTable():
    # creates table items
    c.execute('''CREATE TABLE IF NOT EXISTS items (
        item_id text PRIMARY KEY, item_name text, item_sub_category text,
        cost_quantity int, cost_unit text, weight int,
        item_desc text)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS armor (
        item_id text, armor_id text PRIMARY KEY, armor_category text,
        ac_base int, ac_dex_bon text, ac_dex_bon_max int,
        str_min int, stealth_disadv text)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS weapons (
        item_id text, weapon_id text PRIMARY KEY, weapon_category text,
        category_range text, weapon_range text, max_range int, 
        max_range_disadv int, dmg_dice text, dmg_type text, properties text)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS versatile_weapons (
        item_id text, weapon_id text, twohand_dmg_dice text,
        twohand_dmg_type text)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS thrown_weapons (
        item_id text, weapon_id text, max_throw_range text,
        max_throw_range_disadv text)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS special_weapons (
        item_id text, weapon_id text, special text)''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS vehicles (
        item_id text, vehicle_id text PRIMARY KEY, vehicle_speed int,
        vehicle_unit text)''')
        
    c.execute('''CREATE TABLE IF NOT EXISTS weapon_properties (
        weapon_prop_id text PRIMARY KEY, 
        weapon_prop_name text, weapon_prop_desc text)''')

def dropTables():
    c.execute('DROP TABLE items')
    c.execute('DROP TABLE armor')
    c.execute('DROP TABLE weapons')
    c.execute('DROP TABLE versatile_weapons')
    c.execute('DROP TABLE thrown_weapons')
    c.execute('DROP TABLE special_weapons')
    c.execute('DROP TABLE vehicles')
    c.execute('DROP TABLE weapon_properties')
    
def insertIntoTable(sqlString, tableList):
    c.execute(sqlString, tableList)
    
def dataURL(query):
    url = 'https://www.dnd5eapi.co' + query
    return url
    
def fillWeaponPropTable(json_obj):
    global weaponPropCount
    
    weaponPropID = 'WEPR' + str(weaponPropCount)
    weaponPropName = json_obj['name']
    weaponPropDesc = ''
    for weaponPropIndex in json_obj['desc']:
        weaponPropDesc += weaponPropIndex + ' '
    weaponPropList = [weaponPropID, weaponPropName, weaponPropDesc]
    insertIntoTable('INSERT INTO weapon_properties VALUES (?,?,?)', weaponPropList)
    
    # commit these changes
    conn.commit()
    print('Complete ' + str(weaponPropCount) + '/11')
    weaponPropCount += 1

def dataEntry(json_obj):  
    global count
    global vehicleCount
    global armorCount
    global weaponCount

    # obtain item info
    itemID = 'ITM' + str(count)
    itemName = json_obj['name']
    equipmentCategory = json_obj['equipment_category']['name']

    if(equipmentCategory == 'Weapon'):
        weaponID = 'WP' + str(weaponCount)
        subCategory = json_obj['weapon_category']
        weaponRange = json_obj['weapon_range']
        categoryRange = json_obj['category_range']
        maxRange = json_obj['range']['normal']
        maxRangeDisAdv = json_obj['range']['long']
        if 'damage' in json_obj:
            dmgDice = json_obj['damage']['damage_dice']
            dmgType = json_obj['damage']['damage_type']['name']
        else:
            dmgDice = 'n/a'
            dmgType = 'n/a'
            
        propertyList = []
        if 'properties' in json_obj:
            for propertyIndex in json_obj['properties']:
                propertyList.append(propertyIndex['name'])
                if propertyIndex['name'] == 'Thrown':
                    maxThrowRange = json_obj['throw_range']['normal']
                    maxThrowRangeDisAdv = json_obj['throw_range']['long']
                    
                    # insert into throw weapons table
                    t_weaponList = [itemID, weaponID, maxThrowRange,
                                    maxThrowRangeDisAdv]
                    insertIntoTable('INSERT INTO thrown_weapons VALUES (?,?,?,?)', t_weaponList)
                    
                if propertyIndex['name'] == 'Versatile':
                    twohand_dmg_dice = json_obj['2h_damage']['damage_dice']
                    twohand_dmg_type = json_obj['2h_damage']['damage_type']['name']
                    
                    # insert into versatile weapons table
                    v_weaponList = [itemID, weaponID, twohand_dmg_dice,
                                    twohand_dmg_type]
                    insertIntoTable('INSERT INTO versatile_weapons VALUES (?,?,?,?)', v_weaponList)
                    
                if propertyIndex['name'] == 'Special':
                    special = str(json_obj['special'])
                    
                    # insert into special weapons table
                    s_weaponList = [itemID, weaponID, special]
                    insertIntoTable('INSERT INTO special_weapons VALUES (?,?,?)', s_weaponList)
                    
        
        # insert into weapons table
        weaponList = [itemID, weaponID, subCategory, categoryRange,
                      weaponRange, maxRange, maxRangeDisAdv, 
                      dmgDice, dmgType, str(propertyList)]
        sql = 'INSERT INTO weapons VALUES (?,?,?,?,?,?,?,?,?,?)'
        insertIntoTable(sql, weaponList)
                    
        weaponCount += 1
               
    if(equipmentCategory == 'Armor'):
        subCategory = json_obj['armor_category']
        armorClassBase = json_obj['armor_class']['base']
        armorClassDexBonus = str(json_obj['armor_class']['dex_bonus'])
        armorClassMaxDexBonus = json_obj['armor_class']['max_bonus']
        strMin = json_obj['str_minimum']
        stealthDisAdv = str(json_obj['stealth_disadvantage'])     
        
        # insert into armor table
        armorID = 'ARM' + str(armorCount)
        armorList = [itemID, armorID, subCategory, armorClassBase,
                     armorClassDexBonus, armorClassMaxDexBonus,
                     strMin, stealthDisAdv]
        insertIntoTable('INSERT INTO armor VALUES (?,?,?,?,?,?,?,?)', armorList)
        armorCount += 1
        
    if(equipmentCategory == 'Adventuring Gear'):
        subCategory = json_obj['gear_category']['name']
        
    if(equipmentCategory == 'Tools'):
        subCategory = json_obj['tool_category']
        
    if(equipmentCategory == 'Mounts and Vehicles'):
        subCategory = json_obj['vehicle_category']
        if 'speed' in json_obj:
            vehicleSpeed = json_obj['speed']['quantity']
            vehicleSpeedUnit = json_obj['speed']['unit']
            
            # insert into vehicle table
            vehicleID = 'VHC' + str(vehicleCount)
            vehicleList = [itemID, vehicleID, vehicleSpeed, vehicleSpeedUnit]
            insertIntoTable('INSERT INTO vehicles VALUES (?,?,?,?)', vehicleList)
            vehicleCount += 1
            
    costQuantity = json_obj['cost']['quantity']
    costUnit = json_obj['cost']['unit']
    
    if 'weight' in json_obj:
        weight = json_obj['weight']
    else:
        weight = 0
                
    if 'desc' in json_obj:
        itemDesc = str(json_obj['desc'])
    else:
        itemDesc = 'n/a'
  
# =========================================================================    
    # create the item list and insert into item table
    itemList = [itemID, itemName, subCategory, costQuantity,
                costUnit, weight, itemDesc]
    insertIntoTable('INSERT INTO items VALUES (?,?,?,?,?,?,?)', itemList)
  
# =========================================================================    
    # commit these changes
    conn.commit()
    print('Complete ' + str(count) + '/231')
    count += 1
    
# =========================================================================
# create the table if it doesn't exist
dropTables()
createTable()

# iterate through all the item urls
for itemIndex in json_obj['results']:
    # returns the item url and places it in a json obj
    resp2 = requests.get(dataURL(itemIndex['url']))
    json_obj2 = resp2.json()
    
    # insert data into table
    dataEntry(json_obj2)
    
print('')

# iterate through all the weapon properties
for weaponPropIndex in json_obj3['results']:
    # return the weapon prop urls and place them in a json obj
    resp2 = requests.get(dataURL(weaponPropIndex['url']))
    json_obj4 = resp2.json()
    fillWeaponPropTable(json_obj4)
    
# close out our cursor 
c.close()
conn.close()