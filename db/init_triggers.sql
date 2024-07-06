-- When we need to add lesson
CREATE OR REPLACE FUNCTION check_semester_in_lesson()
RETURNS trigger AS
$$
BEGIN
    -- we check if there was no semestr added
    IF (NEW.semester_id IS NULL) THEN
        -- select new semest_id using borders
        NEW.semester_id = (SELECT semester_id FROM semester 
            WHERE NEW.lesson_date::DATE >= start_date 
                AND NEW.lesson_date::DATE <= end_date LIMIT 1);
        -- if (suddenly) we got null, we raise exception
		IF (NEW.semester_id IS NULL) THEN 
			RAISE EXCEPTION 'Not correct lesson date';
		END IF;
    ELSE 
        -- Here we check, that added lesson and semester has correlation
        -- If not, raise exception
        IF NOT EXISTS (SELECT 1 FROM semester WHERE semester_id = NEW.semester_id AND
                NEW.lesson_date::DATE >= start_date AND NEW.lesson_date::DATE <= end_date) THEN
            RAISE EXCEPTION 'Not correct semester id';
        END IF;
    END IF;

    RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER check_semester_lesson_trigger
    BEFORE INSERT
    ON lesson
    FOR EACH ROW
    EXECUTE PROCEDURE check_semester_in_lesson();

-- Here we have check for semester - is there any overlap with other lessons
CREATE OR REPLACE FUNCTION check_add_lesson()
RETURNS trigger AS
$$
DECLARE
    cur_group INT;
    cur_teacher INT;
BEGIN
    SELECT group_id FROM group_class WHERE class_id=NEW.class_id INTO cur_group;
    SELECT teacher_id FROM group_class WHERE class_id=NEW.class_id INTO cur_teacher;

    IF EXISTS (SELECT 1 FROM lesson l 
            INNER JOIN group_class gc ON gc.class_id = l.class_id
            WHERE (gc.teacher_id = cur_teacher OR gc.group_id = cur_group) AND
            (NEW.lesson_date >= l.lesson_date AND NEW.lesson_date < (l.lesson_date + (INTERVAL '1 min' * l.duration)) OR 
            (NEW.lesson_date + (INTERVAL '1 min' * NEW.duration)) > l.lesson_date AND NEW.lesson_date <= l.lesson_date)) THEN
        RAISE EXCEPTION 'Incorrect lesson start time';
    END IF;

    RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER check_lesson_add
    BEFORE INSERT
    ON lesson
    FOR EACH ROW
    EXECUTE PROCEDURE check_add_lesson();

-- Here we have same check with semester - but if there any overlap with semester
CREATE OR REPLACE FUNCTION check_add_semester()
RETURNS trigger AS
$$
BEGIN
    IF EXISTS (SELECT 1 FROM semester WHERE 
                  NEW.start_date >= start_date AND NEW.start_date < end_date OR 
                  NEW.end_date > start_date AND NEW.end_date <= end_date) THEN
        RAISE EXCEPTION 'Incorrect semester period';
    END IF;

    RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER check_semester_add
    BEFORE INSERT
    ON semester
    FOR EACH ROW
    EXECUTE PROCEDURE check_add_semester();

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

CREATE TRIGGER check_value_of_mark
    BEFORE INSERT
    ON marks_for_visit
    FOR EACH ROW
    EXECUTE PROCEDURE check_mark_value();

CREATE OR REPLACE FUNCTION add_class_to_history()
RETURNS trigger AS
$$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM group_table g 
                      INNER JOIN tracks_type t ON t.track_type_id = g.group_id 
                      WHERE extract(year from OLD.birthday) >= t.start_age AND 
                      extract(year from OLD.birthday) <= t.end_age) THEN
        RAISE EXCEPTION 'Incorrect ';
    END IF;

    INSERT INTO class_history(child_id, class_id, add_date, leave_date) 
        SELECT NEW.child_id AS cid, c.class_id, OLD.add_to_group_date AS add_d, CURRENT_DATE 
		FROM group_class c WHERE group_id = OLD.current_group_id;
    
    NEW.add_to_group_date = CURRENT_DATE;

    RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER add_classes_to_history
    BEFORE UPDATE
    ON child
    FOR EACH ROW
    EXECUTE PROCEDURE add_class_to_history();

CREATE OR REPLACE FUNCTION add_to_history_when_dismissial()
RETURNS trigger AS
$$
BEGIN
    IF (NEW.dismissal_date IS NULL) THEN
        RETURN NEW;
    END IF;

    DELETE FROM worker_by_role WHERE worker_id = OLD.worker_id;

    RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER add_worker_hist_on_dismissial
    BEFORE UPDATE
    ON worker
    FOR EACH ROW
    EXECUTE PROCEDURE add_to_history_when_dismissial();

CREATE OR REPLACE FUNCTION add_to_history_when_delete()
RETURNS trigger AS
$$
BEGIN
    DELETE FROM login_data WHERE worker_id = OLD.worker_id AND level_code = OLD.level_code;

    INSERT INTO worker_history(level_code, worker_id, tensure_start_date, tensure_end_date) VALUES (
        (SELECT w.level_code, w.worker_id, w.tensure_start_date, CURRENT_DATE 
		FROM worker_by_role WHERE group_id = OLD.current_group_id)
	);

    RETURN NEW;
END;
$$
LANGUAGE 'plpgsql';

CREATE TRIGGER add_worker_hist_on_delete
    BEFORE DELETE
    ON worker_by_role
    FOR EACH ROW
    EXECUTE PROCEDURE add_to_history_when_delete();
