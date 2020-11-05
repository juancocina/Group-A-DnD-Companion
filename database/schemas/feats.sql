CREATE TABLE feats (
        feat_id integer PRIMARY KEY, feat_class text, 
        feat_name text, feat_level integer,
        feat_desc text, pre_req_type text, pre_req text,
        grouping text, subclass text, num_you_choose integer,
        list_of_choices text);
