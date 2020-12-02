CREATE TABLE class (
        class_id text PRIMARY KEY, class_name text, hit_die text);
CREATE TABLE prof_choose_from (
        class_id text, num_choices int, prof_choices text);
CREATE TABLE prof_known (
        class_id text, prof_name text);
CREATE TABLE saving_throw_prof (
        class_id text, saving_throw_prof text);
