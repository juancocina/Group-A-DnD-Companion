CREATE TABLE items (
        item_id text PRIMARY KEY, item_name text, item_sub_category text,
        cost_quantity int, cost_unit text, weight int,
        item_desc text);
CREATE TABLE armor (
        item_id text, armor_id text PRIMARY KEY, armor_category text,
        ac_base int, ac_dex_bon text, ac_dex_bon_max int,
        str_min int, stealth_disadv text);
CREATE TABLE weapons (
        item_id text, weapon_id text PRIMARY KEY, weapon_category text,
        category_range text, weapon_range text, max_range int, 
        max_range_disadv int, dmg_dice text, dmg_type text, properties text);
CREATE TABLE versatile_weapons (
        item_id text, weapon_id text, twohand_dmg_dice text,
        twohand_dmg_type text);
CREATE TABLE thrown_weapons (
        item_id text, weapon_id text, max_throw_range text,
        max_throw_range_disadv text);
CREATE TABLE special_weapons (
        item_id text, weapon_id text, special text);
CREATE TABLE vehicles (
        item_id text, vehicle_id text PRIMARY KEY, vehicle_speed int,
        vehicle_unit text);
CREATE TABLE weapon_properties (
        weapon_prop_id text PRIMARY KEY, 
        weapon_prop_name text, weapon_prop_desc text);
