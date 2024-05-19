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

INSERT INTO  app_parent(child_id, name, surname)
    VALUES
    (1, 'Ольга', 'Петрова'),
    (2, 'Михаил', 'Петров'),
    (3, 'Демьян', 'Сидоров'),
    (4, 'Герман', 'Энштейн'),
    (5, 'Валерия', 'Смирнова'),
    (6, 'Павел', 'Морозов');


