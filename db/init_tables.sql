-- all existing tracks (age group)
CREATE TABLE IF NOT EXISTS tracks_type(
    track_type_id SMALLSERIAL PRIMARY KEY,
    start_age SMALLINT NOT NULL,
    end_age SMALLINT NOT NULL CHECK(end_age >= start_age),
    max_lessons_number NUMERIC(1) NOT NULL CHECK(max_lessons_number > 0)
);

-- group of child
CREATE TABLE IF NOT EXISTS group_table(
    group_id SERIAL PRIMARY KEY,
    track_type SMALLINT REFERENCES tracks_type(track_type_id)
);

-- child, educated here
CREATE TABLE IF NOT EXISTS child(
	child_id SERIAL PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    surname VARCHAR(64) NOT NULL,
    patronymic VARCHAR(64),
    birthday DATE NOT NULL CHECK(birthday < CURRENT_DATE),
    current_group_id INT REFERENCES group_table(group_id)
);

-- parent of child
CREATE TABLE IF NOT EXISTS parent(
    parent_id SERIAL PRIMARY KEY,
    child_id INT NOT NULL REFERENCES child(child_id),
    name VARCHAR(64) NOT NULL,
    surname VARCHAR(64) NOT NULL,
    patronymic VARCHAR(64)
);

CREATE TABLE IF NOT EXISTS parent_phones(
    parent_id INT NOT NULL REFERENCES parent(parent_id),
    phone_number CHAR(14) NOT NULL,
    CONSTRAINT unique_phone UNIQUE(parent_id, phone_number)
);

-- worker, here is info about all workers
CREATE TABLE IF NOT EXISTS worker(
    worker_id SERIAL PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    surname VARCHAR(64) NOT NULL,
    patronymic VARCHAR(64),
    hire_date DATE NOT NULL CHECK(hire_date <= CURRENT_DATE),
    dismissal_date DATE CHECK(dismissal_date > hire_date)
);

-- roles of users in system
CREATE TABLE IF NOT EXISTS roles(
    role_name VARCHAR(32) PRIMARY KEY,
    eng_role_name VARCHAR(32) NOT NULL,
    level_code CHAR(1) NOT NULL
);

-- pairs of workers and their roles
CREATE TABLE IF NOT EXISTS worker_by_role(
    role_name VARCHAR(32) NOT NULL REFERENCES roles(role_name),
    worker_id INT NOT NULL REFERENCES worker(worker_id),
    tensure_start_date DATE NOT NULL DEFAULT CURRENT_DATE CHECK(tensure_start_date <= CURRENT_DATE),

    CONSTRAINT primary_worker_role PRIMARY KEY (role_name, worker_id)
);

-- previous pairs of worker and his role
CREATE TABLE IF NOT EXISTS worker_history(
    role_name VARCHAR(32) NOT NULL REFERENCES roles(role_name),
    worker_id INT NOT NULL REFERENCES worker(worker_id),
    tensure_start_date DATE NOT NULL CHECK(tensure_start_date <= CURRENT_DATE),
    tensure_end_date DATE NOT NULL CHECK(tensure_end_date >= tensure_start_date)
);

-- course, written by worker and been studed by child
CREATE TABLE IF NOT EXISTS course(
    course_id SMALLSERIAL PRIMARY KEY,
    course_name VARCHAR(128) NOT NULL
);

-- categories of marks, social etc
CREATE TABLE IF NOT EXISTS mark_categories(
    mark_category VARCHAR(16) PRIMARY KEY,
    description VARCHAR(96) NOT NULL
);

-- fact mark type, like behaviour etc
CREATE TABLE IF NOT EXISTS mark_types(
    mark_type_id SMALLSERIAL PRIMARY KEY,
    description VARCHAR(512) NOT NULL,
    min_value SMALLINT NOT NULL CHECK(min_value >= 0),
    max_value SMALLINT NOT NULL CHECK(max_value > min_value),
    mark_category VARCHAR(16) REFERENCES mark_categories(mark_category)
);

-- which course has which mark types
CREATE TABLE IF NOT EXISTS course_by_mark_types(
    course_id SMALLINT NOT NULL REFERENCES course(course_id),
    mark_type SMALLINT NOT NULL REFERENCES mark_types(mark_type_id),

    CONSTRAINT primary_course_by_mark PRIMARY KEY (course_id, mark_type)
);

-- pair author-course
CREATE TABLE IF NOT EXISTS course_authors(
    course_id SMALLINT NOT NULL REFERENCES course(course_id),
    author_id INT NOT NULL REFERENCES worker(worker_id),

    CONSTRAINT primary_course_by_author PRIMARY KEY (course_id, author_id)
);

-- comnbination of group, teacher (worker with specific type) and course
CREATE TABLE IF NOT EXISTS class(
    class_id BIGSERIAL PRIMARY KEY,
    group_id INT NOT NULL REFERENCES group_table(group_id),
    teacher_id INT NOT NULL REFERENCES worker(worker_id),
    course_id INT NOT NULL REFERENCES course(course_id),
    creation_date DATE NOT NULL,

    CONSTRAINT unique_class UNIQUE(teacher_id, group_id, course_id)
);

-- previous classes, where child was. 
CREATE TABLE IF NOT  EXISTS class_history(
    child_id INT NOT NULL REFERENCES child(child_id),
    class_id INT NOT NULL REFERENCES class(class_id),
    add_date DATE NOT NULL CHECK(add_date <= CURRENT_DATE),
    leave_date DATE NOT NULL CHECK(leave_date >= add_date),

    CONSTRAINT primary_class_history PRIMARY KEY (child_id, class_id)
);

-- comments about course
CREATE TABLE IF NOT EXISTS course_comments(
    course_id INT NOT NULL REFERENCES course(course_id),
    author_id INT NOT NULL REFERENCES worker(worker_id),
    description VARCHAR(512) NOT NULL,

    CONSTRAINT primary_course_comments PRIMARY KEY (course_id, author_id)
);

-- info table for child, like comments
CREATE TABLE IF NOT EXISTS child_info(
    child_id INT NOT NULL REFERENCES child(child_id),
    author_id INT NOT NULL REFERENCES worker(worker_id),
    description VARCHAR(512) NOT NULL,

    CONSTRAINT primary_child_info PRIMARY KEY (child_id, author_id)
);

-- info about class, written by worker
CREATE TABLE IF NOT EXISTS class_info(
    class_id INT NOT NULL REFERENCES class(class_id),
    author_id INT NOT NULL REFERENCES worker(worker_id),
    description VARCHAR(512) NOT NULL,

    CONSTRAINT primary_class_info PRIMARY KEY (class_id, author_id)
);

CREATE TABLE IF NOT EXISTS semester(
    semester_id SERIAL PRIMARY KEY,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL CHECK(end_date > start_date)
);

-- lesson for class
CREATE TABLE IF NOT EXISTS lesson(
    class_id INT NOT NULL REFERENCES class(class_id),
    lesson_date TIMESTAMP NOT NULL,
    duration SMALLINT NOT NULL,
    semester_id INT REFERENCES semester(semester_id),

    CONSTRAINT primary_lesson PRIMARY KEY (class_id, lesson_date)
);

-- written by worker report about class (worker is part of this class)
CREATE TABLE IF NOT EXISTS reports(
    child_id INT NOT NULL REFERENCES child(child_id),
    class_id INT NOT NULL REFERENCES class(class_id),
    semester_id INT NOT NULL REFERENCES semester(semester_id),
    filename VARCHAR(128) NOT NULL, 
    add_time TIME NOT NULL DEFAULT NOW(),

    CONSTRAINT primary_reports PRIMARY KEY (child_id, class_id, semester_id, filename)
);

-- types of class visit, like has visited, has not visited etc
CREATE TABLE IF NOT EXISTS visit_types(
    visit_type_id char(1) PRIMARY KEY,
    description VARCHAR(96) NOT NULL
);

-- fact of visit
CREATE TABLE IF NOT EXISTS visits(
    visit_id BIGSERIAL PRIMARY KEY,
    child_id INT NOT NULL REFERENCES child(child_id),
    class_id INT NOT NULL,
    lesson_date TIMESTAMP NOT NULL,
    visit_type char(1) NOT NULL REFERENCES visit_types(visit_type_id),
	
	CONSTRAINT fk_lessons_from_visits FOREIGN KEY (class_id, lesson_date) REFERENCES lesson(class_id, lesson_date),
    CONSTRAINT unique_visit UNIQUE(child_id, class_id, lesson_date)
);

-- mark for visit
CREATE TABLE IF NOT EXISTS marks_for_visit(
    visit_id BIGINT NOT NULL REFERENCES visits(visit_id),
    mark_type INT NOT NULL REFERENCES mark_types(mark_type_id),
    value SMALLINT NOT NULL
);
