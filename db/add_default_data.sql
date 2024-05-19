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


