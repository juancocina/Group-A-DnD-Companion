CREATE TABLE spells (
        spell_id integer PRIMARY KEY,
        spell_name text, spell_desc text, higher_levels text,
        spell_range text,spell_components text, spell_materials text,
        ritual text, spell_duration text, concentration text,
        casting_time text, spell_level integer, spell_school text);
CREATE TABLE schools_of_magic (
        school_id integer PRIMARY KEY,
        school_name text);
CREATE TABLE classes_spell_list (
        spell_id integer, classes text);
CREATE TABLE damage_spells (
    spell_id integer, attack_type text, damage_type text,
    damage_at_slot_level text, dc_type text,
    dc_success text);
CREATE TABLE dmg_types (
        dmg_type_id integer PRIMARY KEY, dmg_type text);
CREATE TABLE healing_spells (
        spell_id integer PRIMARY KEY,
        heal_at_slot_level text);
