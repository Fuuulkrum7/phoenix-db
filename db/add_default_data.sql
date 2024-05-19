INSERT INTO app_markcategory(mark_category, description) VALUES 
    ('Социальные навыки', 'Навыки, описывающие способность ребенка к корректному социальному взаимодейтсвию'),
    ('Трудное поведение', 'Параметры, отражащии девиации в поведении ребенка');

INSERT INTO app_marktype(description, min_value, max_value, mark_category_id) VALUES
    ('Конструктивно воспринимает неуспех (спокойно реагирует на возникающие проблемы)', 0, 3, 'Социальные навыки'),
    ('Понимает свои границы во время взаимодействия с другими', 0, 3, 'Социальные навыки'),
    ('Понимает чужие границы', 0, 3, 'Социальные навыки'),
    ('Соблюдает правила группы', 0, 3, 'Социальные навыки'),
    ('Участвует в деятельности', 0, 3, 'Социальные навыки'),
    ('Бьет или царапает себя', 0, 3, 'Трудное поведение'),
    ('Бьет, толкает участников группы или ведущих', 0, 3, 'Трудное поведение'),
    ('Громко кричит во время занятия', 0, 3, 'Трудное поведение'),
    ('Игнорирует напоминания о правилах или просьбы ведущего', 0, 3, 'Трудное поведение'),
    ('Кидает, специально ломает вещи', 0, 3, 'Трудное поведение'),
    ('Молча уходит во время задания, молча отказывается от участия в деятельности', 0, 3, 'Трудное поведение'),
    ('Обзывает, оскорбляет участников группы или ведущих, ругается матом, грубо выражается', 0, 3, 'Трудное поведение'),
    ('Отказывается присоединиться к деятельности и заявляет об этом вслух', 0, 3, 'Трудное поведение');

INSERT INTO app_role(role_name, eng_role_name, level_code) VALUES 
    ('Куратор', 'Curator', 'C'),
    ('Ведущий', 'Tutor', 'T'),
    ('Методист', 'Methodist', 'M'),
    ('Администратор', 'Admin', 'A');

INSERT INTO app_tracktype(start_age, end_age, max_lessons_number) VALUES 
    (7, 11, 1),
    (11, 15, 2);

INSERT INTO app_group(group_name, track_type_id)
 VALUES
    ('Дети', (SELECT track_type_id FROM app_tracktype WHERE start_age = 7)),
    ('Подростки', (SELECT track_type_id FROM app_tracktype WHERE start_age = 11));

INSERT INTO app_child(name, surname, birthday, current_group_id, add_to_group_date, gender)
    VALUES
    ('Вася', 'Петров', '01.02.2015', (SELECT group_id from app_group WHERE group_name='Дети'), CURRENT_DATE, 'М'),
    ('Оля', 'Петрова', '05.09.2014', (SELECT group_id from app_group WHERE group_name='Дети'), CURRENT_DATE, 'Ж'),
    ('Вика', 'Сидорова', '03.01.2015', (SELECT group_id from app_group WHERE group_name='Дети'), CURRENT_DATE, 'Ж'),
    ('Альберт', 'Энштейн', '11.02.2010', (SELECT group_id from app_group WHERE group_name='Подростки'), CURRENT_DATE, 'М'),
    ('Федя', 'Смирнов', '01.02.2011', (SELECT group_id from app_group WHERE group_name='Подростки'), CURRENT_DATE, 'М'),
    ('Лена', 'Морозова', '2012.12.21', (SELECT group_id from app_group WHERE group_name='Подростки'), CURRENT_DATE, 'Ж');

INSERT INTO app_parent(child_id, name, surname)
    VALUES
    (1, 'Ольга', 'Петрова'),
    (2, 'Михаил', 'Петров'),
    (3, 'Демьян', 'Сидоров'),
    (4, 'Герман', 'Энштейн'),
    (5, 'Валерия', 'Смирнова'),
    (6, 'Павел', 'Морозов');

INSERT INTO app_parentphone(parent_id, phone_number) 
    VALUES
    (1, '+79845862115'),
    (1, '+75681459578'),
    (2, '+71245891536'),
    (3, '+78432578953'),
    (4, '+78542698289'),
    (4, '+77922277881'),
    (4, '+78963212998'),
    (5, '+79887433012'),
    (5, '+78300945627'),
    (6, '+70012795148');

INSERT INTO app_worker(name, surname, patronymic, hire_date)
    VALUES
    ('Ольга', 'Сидорова', 'Константиновна', CURRENT_DATE),
    ('Нина', 'Разумихина', 'Андреевна', CURRENT_DATE),
    ('Родион', 'Раскольников', 'Романович', CURRENT_DATE),
    ('Борис', 'Федоров', '', CURRENT_DATE);

INSERT INTO app_workerbyrole(level_code_id, worker_id, tensure_start_date)
    VALUES
    ('T', 1, CURRENT_DATE),
    ('M', 1, CURRENT_DATE),
    ('T', 2, CURRENT_DATE),
    ('T', 4, CURRENT_DATE),
    ('M', 2, CURRENT_DATE),
    ('C', 3, CURRENT_DATE);

INSERT INTO app_groupcreator(group_id, curator_id)
    SELECT group_id, 3 as curator FROM group_table;

INSERT INTO app_course(course_name) 
    VALUES
    ('Математика'),
    ('Информатика'),
    ('Грамматика'),
    ('Сеанс психотерапии');

INSERT INTO app_coursebymarktype(course_id, mark_type_id) 
	SELECT a.course_id, b.mark_type_id FROM app_course a, app_marktype b;

INSERT INTO app_courseauthor(course_id, author_id) 
	SELECT a.course_id, b.worker_id FROM app_course a, app_workerbyrole b
    WHERE b.level_code_id = 'M';

INSERT INTO app_groupclass(group_id, teacher_id, course_id, creation_date)
    SELECT g.group_id, w.worker_id, c.course_id, CURRENT_DATE AS cur
    FROM app_group g, app_workerbyrole w, app_course c 
    WHERE w.level_code_id = 'T';

INSERT INTO app_coursecomment(course_id, author_id, description)
    SELECT course_id, 3, 'Все отлично, вы молодцы' FROM app_course; 

INSERT INTO app_classinfo(class_instance_id, author_id, description)
    SELECT c.class_id, w.worker_id, 'Все отлично, вы молодцы' FROM app_groupclass c, app_workerbyrole w
    WHERE w.level_code_id = 'T'; 

INSERT INTO app_childinfo(child_id, author_id, description)
    SELECT c.child_id, w.worker_id, 'Прекрасный ребенок' AS a FROM app_child c, app_worker w; 

INSERT INTO app_semester(start_date, end_date)
    VALUES
    ('2023.06.30', '2023.12.31'),
    ('2024.01.01', '2024.03.30'),
    ('2024.03.31', CURRENT_DATE);


