    CREATE OR REPLACE FUNCTION check_semester_in_lesson()
    RETURNS trigger AS
    $$
    BEGIN
        IF (NEW.semester_id IS NULL) THEN
            SELECT semester_id INTO NEW.semester_id FROM semester 
                WHERE NEW.lesson_date::DATE >= start_date 
                    AND NEW.lesson_date::DATE <= end_date LIMIT 1;
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

CREATE TRIGGER check_semester_lesson_trigger
    BEFORE INSERT
    ON lesson
    FOR EACH ROW
    EXECUTE PROCEDURE check_semester_in_lesson();