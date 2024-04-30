PRAGMA foreign_keys = ON;
------------
create table if not exists task (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL COLLATE NOCASE,
    solver TEXT,
    tests INT,
    generator TEXT,
    jurger TEXT,
    gcount INT,
    interactive INT DEFAULT 0 NOT NULL,
    comp_type TEXT,
    tags INT DEFAULT 0 NOT NULL,
    cpu INT DEFAULT 1000 NOT NULL,
    mem INT DEFAULT 128 NOT NULL,
    qry INT DEFAULT 0 NOT NULL,
    url TEXT DEFAULT '',
    doc TEXT DEFAULT '',
    ctime INT NOT NULL,
    UNIQUE(name),
    CHECK(
        0 <= interactive AND interactive <= 1
    )
);
-- -------
-- create trigger if not exists trg_task_after_insert
-- AFTER INSERT ON task
-- BEGIN
--     UPDATE task SET ctime=unixepoch() WHERE id=NEW.id and ctime is NULL;
-- END;
-- ------
-- create trigger if not exists trg_task_after_update
-- AFTER UPDATE OF content ON task
-- BEGIN
--     UPDATE task SET mtime=unixepoch() WHERE id=NEW.id AND content != OLD.content;
-- END;
-- ------
create index if not exists idx_task_ctime on task(ctime);
-----
-- create index if not exists idx_task_mtime on task(mtime);
------
create index if not exists idx_task_tags on task(tags);
-----
-- create index if not exists idx_task_solved on task(solved);
-----
-- create index if not exists idx_task_level on task(level);
-----
create index if not exists idx_task_interactive on task(interactive);
---------------END TASK-----------------------------------------------
create table if not exists test (
    id INTEGER PRIMARY KEY,
    task_id INT,
    test_id INT,
    checked INT,
    status TEXT,
    input_type TEXT,
    answer_type TEXT,
    FOREIGN KEY(task_id) REFERENCES task(id) ON UPDATE CASCADE ON DELETE CASCADE,
    CHECK(
        0 <= checked AND checked <= 1
    )
);
-----
create index if not exists idx_test_taskid on test(task_id);
---------------END TEST----------------------------------------------
create table if not exists file (
    id INTEGER PRIMARY KEY,
    task_id INT,
    path TEXT,
    content TEXT,
    FOREIGN KEY(task_id) REFERENCES task(id) ON UPDATE CASCADE ON DELETE CASCADE
);
-----
create index if not exists idx_file_taskid on file(task_id);
---------------END FILE----------------------------------------------

---------------BEGIN DIMENSION----------------------------------------------
-- create table if not exists lang (
--     id INTEGER PRIMARY KEY,
--     name TEXT NOT NULL COLLATE NOCASE,
--     solver TEXT NOT NULL,
--     suffix TEXT NOT NULL,
--     template TEXT,
--     debug TEXT,
--     release TEXT,
--     run TEXT NOT NULL,
--     mtime INT,
--     platform TEXT,
--     UNIQUE(name),
--     UNIQUE(suffix)
-- );
-- -----
-- create table if not exists dim_tags (
--     id INTEGER PRIMARY KEY,
--     name TEXT NOT NULL,
--     mtime INT,
--     UNIQUE(name)
-- );
-- -----
-- create table if not exists dim_level (
--     id INTEGER PRIMARY KEY,
--     name TEXT NOT NULL,
--     mtime INT,
--     UNIQUE(name)
-- );
---------------END DIMENSION----------------------------------------------

-- ----- PREPARE DATA
-- insert or replace into task (id, contest, problem) values
--     (1, 'c', 'a'),
--     (2, 'c', 'b');
-- -----
-- insert or replace into file (task_id, name, is_main, content) values
--     (1, 'sol.cpp', 1, 'x\ny'),
--     (1, 'sol.py', 0, ''),
--     (2, 'sol.cpp', 1, '');
-- ---
-- -- update file set content='hi' where task_id=2;
-- -----
-- insert or replace into test (task_id, id, input, expect) values
--     (1, 1, '', ''),
--     (1, 2, '', ''),
--     (2, 1, '', '');
-- -----
-- insert or replace into dim_lang (id, suffix, run, name) values
--     (1, '.cpp', './sol.exe', 'c++'),
--     (2, '.py', 'python sol.py', 'Python');
-- -----
-- insert or replace into dim_temp (lang_id, key, value) values
--     (1, 'single', 'single'),
--     (1, 'multiple', 'multiple');
