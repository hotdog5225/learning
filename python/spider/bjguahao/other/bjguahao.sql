CREATE TABLE hospital(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) not null DEFAULT '',
    hosp_id bigint not null default 0,
    level varchar(256) not null default '',
    open_text varchar(256) not null default '',
    unique key uniq_hosp_id (hosp_id)
);

CREATE TABLE department(
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) not null DEFAULT '',
    dept_code_1 bigint not null default 0,
    dept_code_2 bigint not null default 0,
    level varchar(256) not null default '',
    hot_dept bool default false,
    unique key uniq_dept_code_1_dept_code_2 (dept_code_1, dept_code_2),
    index idx_dept_code_2 (dept_code_2)
);