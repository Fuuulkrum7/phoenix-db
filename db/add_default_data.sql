INSERT INTO mark_categories(mark_category, description) VALUES 
    ('Социальные навыки', 'Навыки, описывающие способность ребенка к корректному социальному взаимодейтсвию'),
    ('Трудное поведение', 'Параметры, отражащии девиации в поведении ребенка');

INSERT INTO mark_types(description, min_value, max_value, mark_category) VALUES
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

INSERT INTO roles(role_name, eng_role_name, level_code) VALUES 
    ('Куратор', 'Curator', 'C'),
    ('Ведущий', 'Tutor', 'T'),
    ('Методист', 'Methodist', 'M'),
    ('Администратор', 'Admin', 'A');

INSERT INTO track_type(start_age, end_age, max_lessons_number) VALUES 
    (7, 11, 1),
    (11, 15, 2);

INSERT INTO group_table(group_name, track_type)
 VALUES
    ('Дети', (SELECT track_type_id FROM track_type WHERE start_age = 7)),
    ('Подростки', (SELECT track_type_id FROM track_type WHERE start_age = 11));

INSERT INTO child(name, surname, birthday, current_group_id, add_to_group_date, gender)
    VALUES
    ('Вася', 'Петров', '01.02.2015', (SELECT group_id from group_table WHERE group_name='Дети'), CURRENT_DATE, 'М'),
    ('Оля', 'Петрова', '05.09.2014', (SELECT group_id from group_table WHERE group_name='Дети'), CURRENT_DATE, 'Ж'),
    ('Вика', 'Сидорова', '03.01.2015', (SELECT group_id from group_table WHERE group_name='Дети'), CURRENT_DATE, 'Ж'),
    ('Альберт', 'Энштейн', '11.02.2010', (SELECT group_id from group_table WHERE group_name='Подростки'), CURRENT_DATE, 'М'),
    ('Федя', 'Смирнов', '01.02.2011', (SELECT group_id from group_table WHERE group_name='Подростки'), CURRENT_DATE, 'М'),
    ('Лена', 'Морозова', '2012.12.21', (SELECT group_id from group_table WHERE group_name='Подростки'), CURRENT_DATE, 'Ж');

INSERT INTO parent(name, surname, role)
    VALUES
    ('Ольга', 'Петрова', 'Мама'),
    ('Михаил', 'Петров', 'Папа'),
    ('Демьян', 'Сидоров', 'Брат'),
    ('Герман', 'Энштейн', 'Дед'),
    ('Валерия', 'Смирнова', 'Бабушка'),
    ('Павел', 'Морозов', 'Лучший друг');

INSERT INTO parent_by_child(child_id, parent_id) 
	SELECT a.child_id, b.parent_id FROM child a, parent b;

INSERT INTO parent_phones(parent_id, phone_number) 
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

INSERT INTO worker(name, surname, patronymic, hire_date)
    VALUES
    ('Ольга', 'Сидорова', 'Константиновна', CURRENT_DATE),
    ('Нина', 'Разумихина', 'Андреевна', CURRENT_DATE),
    ('Родион', 'Раскольников', 'Романович', CURRENT_DATE),
    ('Борис', 'Федоров', '', CURRENT_DATE);

INSERT INTO worker_by_role(level_code, worker_id, tensure_start_date)
    VALUES
    ('T', 1, CURRENT_DATE),
    ('M', 1, CURRENT_DATE),
    ('T', 2, CURRENT_DATE),
    ('T', 4, CURRENT_DATE),
    ('M', 2, CURRENT_DATE),
    ('C', 3, CURRENT_DATE);

INSERT INTO group_creators(group_id, curator_id)
    SELECT group_id, 3 as curator FROM group_table;

INSERT INTO course(course_name) 
    VALUES
    ('Математика'),
    ('Информатика'),
    ('Грамматика'),
    ('Сеанс психотерапии');

INSERT INTO course_by_mark_types(course_id, mark_type) 
	SELECT a.course_id, b.mark_type_id FROM course a, mark_types b;

INSERT INTO course_authors(course_id, author_id) 
	SELECT a.course_id, b.worker_id FROM course a, worker_by_role b
    WHERE b.level_code = 'M';

INSERT INTO group_class(group_id, teacher_id, course_id, creation_date)
    SELECT g.group_id, w.worker_id, c.course_id, CURRENT_DATE AS cur
    FROM group_table g, worker_by_role w, course c 
    WHERE w.level_code = 'T';

INSERT INTO course_comments(course_id, author_id, description)
    SELECT course_id, 3, 'Все отлично, вы молодцы' FROM course; 

INSERT INTO class_info(class_id, author_id, description)
    SELECT c.class_id, w.worker_id, 'Все отлично, вы молодцы' FROM group_class c, worker_by_role w
    WHERE w.level_code = 'T'; 

INSERT INTO child_info(child_id, author_id, description)
    SELECT c.child_id, w.worker_id, 'Прекрасный ребенок' AS a FROM child c, worker w; 

INSERT INTO semester(start_date, end_date)
    VALUES
    ('2023.06.30', '2023.12.31'),
    ('2024.01.01', '2024.03.30'),
    ('2024.03.31', CURRENT_DATE),
    (CURRENT_DATE, '2024.06.30');

INSERT INTO login_data VALUES
  ('admin', 1);

INSERT INTO lesson (class_id, lesson_date, duration, semester_id) VALUES 
    (1, '2024-05-20 09:00:00', 40, 4),
    (1, '2024-05-20 10:00:00', 40, 4),

    -- Tuesday
    (1, '2024-05-21 11:00:00', 40, 4),
    (1, '2024-05-21 12:00:00', 40, 4),

    -- Wednesday
    (1, '2024-05-22 13:00:00', 40, 4),
    (1, '2024-05-22 14:00:00', 40, 4),

    -- Thursday
    (1, '2024-05-23 15:00:00', 40, 4),
    (1, '2024-05-23 16:00:00', 40, 4),

    -- Friday
    (1, '2024-05-24 17:00:00', 40, 4),
    (1, '2024-05-24 18:00:00', 40, 4);

