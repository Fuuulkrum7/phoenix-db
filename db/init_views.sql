CREATE VIEW getAllStats AS
    SELECT v.visit_id, v.child_id, v.class_id, v.lesson_date, v.visit_type, 
	m.mark_type, m.mark, t.description, t.mark_category 
	FROM visits v 
    INNER JOIN marks_for_visit m ON m.visit_id = v.visit_id 
    INNER JOIN mark_types t ON t.mark_type_id = m.mark_type; 