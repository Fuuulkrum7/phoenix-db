CREATE INDEX index_class_history ON class_history(child_id, class_id);

CREATE INDEX index_child_group ON child(current_group_id);

CREATE INDEX index_class_u ON group_class(teacher_id, group_id, course_id);

CREATE INDEX index_parent_phones_u ON parent_phones(parent_id, phone_number);
CREATE INDEX index_parent_f ON parent(child_id);

CREATE INDEX index_visits_u ON visits(child_id, class_id, lesson_date);
CREATE INDEX index_visits_by_lesson ON visits(class_id, lesson_date);

-- That's a good point - we change lessons some times per day,
-- but we also search them more times per day
-- CREATE INDEX index_lessons_date ON lesson(lesson_date);
-- CREATE INDEX index_lesson_by_semester_and_class ON lesson(semester_id, class_id);

CREATE INDEX index_reports_by_class_and_semester ON reports(class_id, semester_id);

CREATE INDEX index_marks_value ON marks_for_visit(mark);

CREATE INDEX index_semester_start ON semester(start_date);
