from django.db import migrations, models

def create_postgresql_triggers(apps, schema_editor):
    # Function to check semester in lesson
    schema_editor.execute('''
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
    ''')

    # Function to check mark value
    schema_editor.execute('''
    CREATE OR REPLACE FUNCTION check_mark_value()
    RETURNS trigger AS
    $$
    BEGIN
        IF EXISTS(SELECT 1 FROM mark_types WHERE NEW.mark > max_value) THEN
            RAISE EXCEPTION 'Too big mark has been added';
        END IF;

        RETURN NEW;
    END;
    $$
    LANGUAGE 'plpgsql';
    ''')

    # Function to add class to history
    schema_editor.execute('''
    CREATE OR REPLACE FUNCTION add_class_to_history()
    RETURNS trigger AS
    $$
    BEGIN
        INSERT INTO class_history(child_id, class_id, add_date, leave_date) VALUES (
            (SELECT NEW.child_id AS cid, c.class_id, OLD.add_to_group_date AS add_d, CURRENT_DATE 
            FROM group_class c WHERE group_id = OLD.current_group_id)
        );

        NEW.add_to_group_date = CURRENT_DATE;

        RETURN NEW;
    END;
    $$
    LANGUAGE 'plpgsql';
    ''')

    # Function to add to history when dismissal
    schema_editor.execute('''
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
    ''')

    # Function to add to history when delete
    schema_editor.execute('''
    CREATE OR REPLACE FUNCTION add_to_history_when_delete()
    RETURNS trigger AS
    $$
    BEGIN
        INSERT INTO worker_history(role_name, worker_id, tensure_start_date, tensure_end_date) VALUES (
            (SELECT w.role_name, w.worker_id, w.tensure_start_date, CURRENT_DATE 
            FROM worker_by_role WHERE group_id = OLD.current_group_id)
        );

        RETURN NEW;
    END;
    $$
    LANGUAGE 'plpgsql';
    ''')

    # Trigger to check semester in lesson
    schema_editor.execute('''
    CREATE TRIGGER check_semester_lesson_trigger
        BEFORE INSERT
        ON lesson
        FOR EACH ROW
        EXECUTE PROCEDURE check_semester_in_lesson();
    ''')

    # Trigger to check mark value
    schema_editor.execute('''
    CREATE TRIGGER check_value_of_mark
        BEFORE INSERT
        ON marks_for_visit
        FOR EACH ROW
        EXECUTE PROCEDURE check_mark_value();
    ''')

    # Trigger to add classes to history
    schema_editor.execute('''
    CREATE TRIGGER add_classes_to_history
        BEFORE UPDATE
        ON child
        FOR EACH ROW
        EXECUTE PROCEDURE add_class_to_history();
    ''')

    # Trigger to add worker history on delete
    schema_editor.execute('''
    CREATE TRIGGER add_worker_hist_on_delete
        BEFORE DELETE
        ON worker_by_role
        FOR EACH ROW
        EXECUTE PROCEDURE add_to_history_when_delete();
    ''')

    # Trigger to add worker history on dismissal
    schema_editor.execute('''
    CREATE TRIGGER add_worker_hist_on_dismissial
        BEFORE UPDATE
        ON worker
        FOR EACH ROW
        EXECUTE PROCEDURE add_to_history_when_dismissial();
    ''')

class Migration(migrations.Migration):

    dependencies = [
        ('your_app_name', 'previous_migration_file'),
    ]

    operations = [
        migrations.RunSQL(
            create_postgresql_triggers,
            reverse_sql='''
            DROP TRIGGER IF EXISTS check_semester_lesson_trigger ON lesson;
            DROP TRIGGER IF EXISTS check_value_of_mark ON marks_for_visit;
            DROP TRIGGER IF EXISTS add_classes_to_history ON child;
            DROP TRIGGER IF EXISTS add_worker_hist_on_delete ON worker_by_role;
            DROP TRIGGER IF EXISTS add_worker_hist_on_dismissial ON worker;
            DROP FUNCTION IF EXISTS check_semester_in_lesson();
            DROP FUNCTION IF EXISTS check_mark_value();
            DROP FUNCTION IF EXISTS add_class_to_history();
            DROP FUNCTION IF EXISTS add_to_history_when_dismissial();
            DROP FUNCTION IF EXISTS add_to_history_when_delete();
            '''
        ),
    ]
