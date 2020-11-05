CREATE TABLE race (
        race_id text PRIMARY KEY, race_name text, speed int, 
        alignment text, age text, size text, size_desc text, 
        lang_desc text);
CREATE TABLE traits_known (
        race_id text, trait_id text);
CREATE TABLE traits_choose_from (
        race_id text, pick_num_traits int, trait_option_id text);
CREATE TABLE starting_prof (
        race_id text, proficiency text);
CREATE TABLE stat_bonuses (
        race_id text, stat_name text, bonus int);
CREATE TABLE languages (
        lang_id text PRIMARY KEY, lang text);
CREATE TABLE languages_known (
        race_id text, lang_id text);
CREATE TABLE lang_choose_from (
        race_id text, pick_num_lang int, lang_option_id text);
