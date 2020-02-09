CREATE TABLE sct_description_term
SELECT * FROM nhs_dbs.sct_description_output WHERE TypeId='900000000000003001' AND Term REGEXP '.*(finding)|.*(disorder)|.*(situation)'