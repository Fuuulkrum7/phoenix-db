CREATE OR REPLACE FUNCTION check_semester_in_lesson()
RETURNS trigger AS
$$
BEGIN
    IF (NEW.semester_id IS NULL) THEN
        NEW.semester_id = (SELECT semester_id FROM semester 
            WHERE NEW.lesson_date::DATE >= start_date 
                AND NEW.lesson_date::DATE <= end_date LIMIT 1);
		IF (NEW.semester_id IS NULL) THEN 
			RAISE EXCEPTION 'Not correct lesson date';
		END IF;
    ELSE 
        IF NOT EXISTS (SELECT 1 FROM semester WHERE semester_id = NEW.semester_id AND
                NEW.lesson_date::DATE >= start_date AND NEW.lesson_date::DATE <= end_date) THEN
            RAISE EXCEPTION 'Not correct semester id';
        END IF;
    END IF;

    RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION check_mark_value()
RETURNS trigger AS
$$
BEGIN
    iF EXISTS(SELECT 1 FROM mark_types WHERE NEW.mark > max_value) THEN
        RAISE EXCEPTION 'To big mark has been added';
    END IF;

    RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

CREATE OR REPLACE FUNCTION add_class_to_history()
RETURNS trigger AS
$$
BEGIN
    INSERT INTO class_history(child_id, class_id, add_date, leave_date) VALUES (
        (SELECT NEW.child_id AS cid, c.class_id, OLD.add_to_group_date AS add_d, CURRENT_DATE 
		FROM group_class WHERE group_id = OLD.current_group_id)
	);
    
    NEW.add_to_group_date = CURRENT_DATE;

    RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

-- CREATE OR REPLACE FUNCTION add_worker_to_history()
-- RETURNS trigger AS
-- $$
-- BEGIN
--     INSERT INTO worker_history(role_name, worker_id, tensure_start_date, tensure_end_date) VALUES (
--         (SELECT NEW.worker_id AS cid, c.class_id, OLD.add_to_group_date AS add_d, CURRENT_DATE 
-- 		FROM group_class WHERE group_id = OLD.current_group_id)
-- 	);
    
--     NEW.add_to_group_date = CURRENT_DATE;

--     RETURN NEW;
-- END;
-- $$
-- LANGUAGE 'plpgsql';

CREATE TRIGGER check_semester_lesson_trigger
    BEFORE INSERT
    ON lesson
    FOR EACH ROW
    EXECUTE PROCEDURE check_semester_in_lesson();

CREATE TRIGGER check_value_of_mark
    BEFORE INSERT
    ON marks_for_visit
    FOR EACH ROW
    EXECUTE PROCEDURE check_mark_value();

CREATE TRIGGER add_classes_to_history
    BEFORE UPDATE
    ON child
    FOR EACH ROW
    EXECUTE PROCEDURE add_class_to_history();
