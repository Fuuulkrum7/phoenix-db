CREATE VIEW getAllStats AS
    SELECT * FROM visits v 
    INNER JOIN marks_for_visit m ON m.visit_id = v.visit_id 
    INNER JOIN mark_types t ON t.mark_type_id = m.mark_type; 