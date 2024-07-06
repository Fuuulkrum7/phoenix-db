from django.db import models
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from django.db.models import Avg

# TODO add indexes

## \class TrackType
## \brief Represents the types of tracks for different age groups.
class TrackType(models.Model):
    track_type_id = models.AutoField(primary_key=True, db_column="track_type_id")
    start_age = models.SmallIntegerField(null=False, db_column="start_age")
    end_age = models.SmallIntegerField(null=False, db_column="end_age")
    max_lessons_number = models.DecimalField(
        max_digits=1, decimal_places=0, null=False, db_column="max_lessons_number")

    class Meta:
        db_table = "track_type"
        constraints = [
            models.CheckConstraint(check=models.Q(start_age__gt=0), name='check_start_age_gt_0'),
            models.CheckConstraint(check=models.Q(end_age__gte=models.F('start_age')), name='check_end_age_gte_start_age'),
            models.CheckConstraint(check=models.Q(max_lessons_number__gt=0), name='check_max_lessons_number_gt_0'),
            models.UniqueConstraint(fields=['start_age', 'end_age'], name='unique_age')
        ]

## \class Group
## \brief Represents a group of children.
class Group(models.Model):
    group_id = models.AutoField(primary_key=True, db_column="group_id")
    group_name = models.CharField(max_length=64, null=False, db_column="group_name")
    track_type = models.ForeignKey(TrackType, on_delete=models.CASCADE, db_column="track_type")
    
    class Meta:
        db_table = "group_table"


## \class Child
## \brief Represents a child_id enrolled in the system.
class Child(models.Model):
    child_id = models.AutoField(primary_key=True, db_column="child_id")
    name = models.CharField(max_length=64, null=False, db_column="name")
    surname = models.CharField(max_length=64, null=False, db_column="surname")
    patronymic = models.CharField(max_length=64, blank=True, null=True, db_column="patronymic")
    birthday = models.DateField(null=False, db_column="birthday")
    current_group = models.ForeignKey(
        Group, on_delete=models.CASCADE, null=True, db_column="current_group_id")
    add_to_group_date = models.DateField(auto_now_add=True, null=True, db_column="add_to_group_date")
    gender = models.CharField(max_length=1, null=False, db_column="gender")
    
    class Meta:
        db_table = "child"
        
        indexes = [
            models.Index(fields=['current_group']),
        ]
        
        constraints = [
            models.CheckConstraint(check=models.Q(birthday__lt=models.functions.Now()), name='check_birthday_lt_current_date')
        ]

## \class Parent
## \brief Represents a parent of a child.
class Parent(models.Model):
    parent_id = models.AutoField(primary_key=True, db_column="parent_id")
    name = models.CharField(max_length=64, null=False, db_column="name")
    surname = models.CharField(max_length=64, null=False, db_column="surname")
    patronymic = models.CharField(max_length=64, blank=True, null=True, db_column="patronymic")
    role = models.CharField(max_length=64, null=True, db_column="role")
    
    class Meta:
        db_table = "parent"

class ParentByChild(models.Model):
    parent_id = models.ForeignKey(Parent, on_delete=models.CASCADE, db_column="parent_id")
    child_id = models.ForeignKey(Child, on_delete=models.CASCADE, db_column="child_id")

    class Meta:
        db_table = "parent_by_child"
        
        constraints = [
            models.UniqueConstraint(fields=['parent_id', 'child_id'], name='primary_parent_by_child')
        ]
        
        indexes = [
            models.Index(fields=['child_id', 'parent_id']),
        ]

## \class ParentPhone
## \brief Represents the phone number of a parent.
class ParentPhone(models.Model):
    parent_id = models.ForeignKey(Parent, on_delete=models.CASCADE, db_column="parent_id")
    phone_number = models.CharField(max_length=14, null=False, db_column="phone_number")

    class Meta:
        db_table = "parent_phones"
        
        constraints = [
            models.UniqueConstraint(fields=['parent_id', 'phone_number'], name='unique_parent_phone')
        ]
        
        indexes = [
            models.Index(fields=['parent_id', 'phone_number']),
        ]

## \class Worker
## \brief Represents a worker in the system.
class Worker(models.Model):
    worker_id = models.AutoField(primary_key=True, db_column="worker_id")
    name = models.CharField(max_length=64, null=False, db_column="name")
    surname = models.CharField(max_length=64, null=False, db_column="surname")
    patronymic = models.CharField(max_length=64, blank=True, null=True, db_column="patronymic")
    hire_date = models.DateField(null=False, db_column="hire_date")
    dismissal_date = models.DateField(blank=True, null=True, db_column="dismissal_date")

    class Meta:
        db_table = "worker"
        
        constraints = [
            models.CheckConstraint(check=models.Q(hire_date__lte=models.functions.Now()), name='check_hire_date_le_current_date'),
            models.CheckConstraint(check=models.Q(dismissal_date__gt=models.F('hire_date')), name='check_dismissal_date_gt_hire_date')
        ]

## \class Role
## \brief Represents a role in the system.
class Role(models.Model):
    level_code = models.CharField(max_length=1, primary_key=True, db_column="level_code")
    role_name = models.CharField(max_length=32, unique=True, null=False, db_column="role_name")
    eng_role_name = models.CharField(max_length=32, null=False, db_column="eng_role_name")
    
    class Meta:
        db_table = "roles"


## \class WorkerByRole
## \brief Represents the association of a worker with a role.
class WorkerByRole(models.Model):
    level_code = models.ForeignKey(Role, on_delete=models.CASCADE, db_column="level_code")
    worker_id = models.ForeignKey(Worker, on_delete=models.CASCADE, db_column="worker_id")
    tensure_start_date = models.DateField(auto_now_add=True, db_column="tensure_start_date")

    class Meta:
        db_table = "worker_by_role"
        
        constraints = [
            models.CheckConstraint(check=models.Q(tensure_start_date__lte=models.functions.Now()), name='check_tens_st_date_le_curr_date'),
            models.UniqueConstraint(fields=['level_code', 'worker_id'], name='primary_worker_role')
        ]
        
        indexes = [
            models.Index(fields=['worker_id', 'level_code']),
        ]

## \class LoginData
## \brief Represents login data for a worker.
class LoginData(models.Model):
    worker_login = models.CharField(max_length=64, primary_key=True, db_column="worker_login")
    worker_id = models.ForeignKey(Worker, on_delete=models.CASCADE, db_column="worker_id")
    
    class Meta:
        db_table = "login_data"


## \class WorkerHistory
## \brief Represents the history of a worker's roles.
class WorkerHistory(models.Model):
    worker_id = models.ForeignKey(Worker, on_delete=models.CASCADE, db_column="worker_id")
    level_code = models.ForeignKey(Role, on_delete=models.CASCADE, db_column="level_code")
    tensure_start_date = models.DateField(null=False, db_column="tensure_start_date")
    tensure_end_date = models.DateField(null=False, db_column="tensure_end_date")

    class Meta:
        db_table = "worker_by_history"
        
        constraints = [
            models.CheckConstraint(
                check=models.Q(tensure_start_date__lte=models.functions.Now()), 
                name='check_tensure_start_date_le_current_date'),
            
            models.CheckConstraint(
                check=models.Q(tensure_end_date__gte=models.F('tensure_start_date')), 
                name='check_tensure_end_date_ge_tensure_start_date'),
            
            models.UniqueConstraint(
                fields=['worker_id', 'level_code', 'tensure_start_date'], name='unique_level_worker_tensure_date'
            )
        ]
        
        indexes = [
            models.Index(fields=['worker_id', 'level_code', 'tensure_start_date']),
        ]

## \class Course
## \brief Represents a course.
class Course(models.Model):
    course_id = models.AutoField(primary_key=True, db_column="course_id")
    course_name = models.CharField(max_length=128, null=False, db_column="course_name")

    class Meta:
        db_table = "course"

## \class MarkCategory
## \brief Represents a category of marks.
class MarkCategory(models.Model):
    mark_category = models.CharField(max_length=32, primary_key=True, db_column="mark_category")
    description = models.CharField(max_length=96, null=False, db_column="description")

    class Meta:
        db_table = "mark_categories"

## \class MarkType
## \brief Represents a type of mark.
class MarkType(models.Model):
    mark_type_id = models.AutoField(primary_key=True, db_column="mark_type_id")
    description = models.CharField(max_length=512, null=False, db_column="description")
    min_value = models.SmallIntegerField(null=False, db_column="min_value")
    max_value = models.SmallIntegerField(null=False, db_column="max_value")
    mark_category = models.ForeignKey(
        MarkCategory, on_delete=models.CASCADE, db_column="mark_category")

    class Meta:
        db_table = "mark_types"
        
        constraints = [
            models.CheckConstraint(check=models.Q(min_value__gte=0), name='check_min_value_gte_0'),
            models.CheckConstraint(check=models.Q(max_value__gt=models.F('min_value')), name='check_max_value_gt_min_value')
        ]

## \class CourseByMarkType
## \brief Represents the association of a course with mark types.
class CourseByMarkType(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, db_column="course_id")
    mark_type = models.ForeignKey(MarkType, on_delete=models.CASCADE, db_column="mark_type")

    class Meta:
        db_table = "course_by_mark_types"
        
        constraints = [
            models.UniqueConstraint(fields=['course_id', 'mark_type'], name='primary_course_by_mark')
        ]

## \class CourseAuthor
## \brief Represents the authorship of a course.
class CourseAuthor(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, db_column="course_id")
    author_id = models.ForeignKey(Worker, on_delete=models.CASCADE, db_column="author_id")

    class Meta:
        db_table = "course_authors"
        
        constraints = [
            models.UniqueConstraint(fields=['course_id', 'author_id'], name='primary_course_by_author')
        ]
        
        indexes = [
            models.Index(fields=['author_id', 'course_id']),
        ]

## \class GroupClass
## \brief Represents a class within a group, associated with a teacher and a course.
class GroupClass(models.Model):
    class_id = models.AutoField(primary_key=True, db_column="class_id")
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE, db_column="group_id")
    teacher_id = models.ForeignKey(Worker, on_delete=models.CASCADE, db_column="teacher_id")
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, db_column="course_id")
    creation_date = models.DateField(null=False, db_column="creation_date")

    class Meta:
        db_table = "group_class"
        
        constraints = [
            models.UniqueConstraint(fields=['teacher_id', 'group_id', 'course_id'], name='unique_class')
        ]
        
        indexes = [
            models.Index(fields=['teacher_id', 'group_id', 'course_id']),
        ]

## \class ClassHistory
## \brief Represents the history of classes a child has been in.
class ClassHistory(models.Model):
    child_id = models.ForeignKey(Child, on_delete=models.CASCADE, db_column="child_id")
    class_id = models.ForeignKey(GroupClass, on_delete=models.CASCADE, db_column="class_id")
    add_date = models.DateField(null=False, db_column="add_date")
    leave_date = models.DateField(null=False, db_column="leave_date")

    class Meta:
        db_table = "class_history"
        
        constraints = [
            models.CheckConstraint(check=models.Q(add_date__lte=models.functions.Now()), name='check_add_date_le_current_date'),
            models.CheckConstraint(check=models.Q(leave_date__gte=models.F('add_date')), name='check_leave_date_ge_add_date'),
            models.UniqueConstraint(fields=['child_id', 'class_id'], name='primary_class_history')
        ]
        
        indexes = [
            models.Index(fields=['child_id', 'class_id']),
        ]

## \class CourseComment
## \brief Represents comments about a course.
class CourseComment(models.Model):
    course_id = models.ForeignKey(Course, on_delete=models.CASCADE, db_column="course_id")
    author_id = models.ForeignKey(Worker, on_delete=models.CASCADE, db_column="author_id")
    description = models.CharField(max_length=512, null=False, db_column="")

    class Meta:
        db_table = "course_comments"
        
        constraints = [
            models.UniqueConstraint(fields=['course_id', 'author_id'], name='primary_course_comments')
        ]
        
        indexes = [
            models.Index(fields=['course_id', 'author_id']),
        ]

## \class ChildInfo
## \brief Represents information about a child, such as comments.
class ChildInfo(models.Model):
    child_id = models.ForeignKey(Child, on_delete=models.CASCADE, db_column="child_id")
    author_id = models.ForeignKey(Worker, on_delete=models.CASCADE, db_column="author_id")
    description = models.CharField(max_length=512, null=False, db_column="description")

    class Meta:
        db_table = "child_info"
        
        constraints = [
            models.UniqueConstraint(fields=['child_id', 'author_id'], name='primary_child_info')
        ]
        
        indexes = [
            models.Index(fields=['child_id', 'author_id']),
        ]

## \class ClassInfo
## \brief Represents information about a class, written by a worker.
class ClassInfo(models.Model):
    class_id = models.ForeignKey(GroupClass, on_delete=models.CASCADE, db_column="class_id")
    author_id = models.ForeignKey(Worker, on_delete=models.CASCADE, db_column="author_id")
    description = models.CharField(max_length=512, null=False, db_column="description")

    class Meta:
        db_table = "class_info"
        
        constraints = [
            models.UniqueConstraint(fields=['class_id', 'author_id'], name='primary_class_info')
        ]
        
        indexes = [
            models.Index(fields=['class_id', 'author_id']),
        ]

## \class Semester
## \brief Represents a semester with a start and end date.
class Semester(models.Model):
    semester_id = models.AutoField(primary_key=True, db_column="semester_id")
    start_date = models.DateField(null=False, db_column="start_date")
    end_date = models.DateField(null=False, db_column="end_date")

    class Meta:
        db_table = "semester"
        
        constraints = [
            models.CheckConstraint(check=models.Q(end_date__gt=models.F('start_date')), name='check_end_date_gt_start_date')
        ]

## \class Lesson
## \brief Represents a lesson for a class within a semester.
class Lesson(models.Model):
    class_id = models.ForeignKey(GroupClass, on_delete=models.CASCADE, db_column="class_id")
    lesson_date = models.DateTimeField(null=False, db_column="lesson_date")
    duration = models.SmallIntegerField(null=False, db_column="duration")
    semester = models.ForeignKey(
        Semester, on_delete=models.CASCADE, blank=True, null=True, db_column="semester_id")

    class Meta:
        db_table = "lesson"
        
        constraints = [
            models.UniqueConstraint(fields=['class_id', 'lesson_date'], name='primary_lesson')
        ]

## \class Report
## \brief Represents a report written by a worker about a class.
class Report(models.Model):
    child_id = models.ForeignKey(Child, on_delete=models.CASCADE, db_column="child_id")
    class_id = models.ForeignKey(GroupClass, on_delete=models.CASCADE, db_column="class_id")
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, db_column="semester_id")
    filename = models.CharField(max_length=128, null=False, db_column="filename")
    add_time = models.TimeField(auto_now_add=True, db_column="add_time")

    class Meta:
        db_table = "report"
        
        constraints = [
            models.UniqueConstraint(fields=['child_id', 'class_id', 'semester', 'filename'], name='primary_reports')
        ]
        
        indexes = [
            models.Index(fields=['class_id', 'semester']),
            models.Index(fields=['child_id', 'class_id', 'semester', 'filename'])
        ]

## \class Visit
## \brief Represents a visit record for a child to a lesson.
class Visits(models.Model):
    visit_id = models.AutoField(primary_key=True, db_column="visit_id")
    child_id = models.ForeignKey(Child, on_delete=models.CASCADE, db_column="child_id")
    class_id = models.ForeignKey(GroupClass, on_delete=models.CASCADE, db_column="class_id")
    lesson_date = models.DateTimeField(null=False, db_column="lesson_date")
    description = models.CharField(max_length=96, null=True, db_column="description")
    visited = models.BooleanField(default=True, db_column="visited")

    class Meta:
        db_table = "visits"
        
        constraints = [
            models.UniqueConstraint(fields=['child_id', 'class_id', 'lesson_date'], name='unique_visit')
        ]
        
        indexes = [
            models.Index(fields=['child_id', 'class_id', 'lesson_date']),
            models.Index(fields=['class_id', 'lesson_date'])
        ]
    
    def clean(self):
        super().clean()
        if not Lesson.objects.filter(class_id=self.class_id, lesson_date=self.lesson_date).exists():
            raise ValidationError('Invalid combination of class_id and lesson_date.')

@receiver(pre_save, sender=Visits)
def validate_visit(sender, instance, **kwargs):
    instance.clean()

## \class GroupCreators
## \brief Represents the association between a group and its curator.
class GroupCreators(models.Model):
    group_id = models.ForeignKey(Group, on_delete=models.CASCADE, db_column="group_id")
    curator_id = models.ForeignKey(Worker, on_delete=models.CASCADE, db_column="curator_id")

    class Meta:
        db_table = "group_creators"
        
        constraints = [
            models.UniqueConstraint(fields=['group_id', 'curator_id'], name='primary_group_by_creator')
        ]
        
        indexes = [
            models.Index(fields=['group_id', 'curator_id']),
        ]

## \class MarksForVisit
## \brief Represents marks given for a visit.
class MarksForVisit(models.Model):
    visit = models.ForeignKey(Visits, on_delete=models.CASCADE, db_column="visit_id") ## \brief Foreign key to Visits.
    mark_type = models.ForeignKey(MarkType, on_delete=models.CASCADE, db_column="mark_type") ## \brief Foreign key to MarkTypes.
    mark = models.DecimalField(max_digits=3, decimal_places=1, db_column="mark") ## \brief The mark given.
    
    class Meta:
        db_table = "marks_for_visit"
    
    @classmethod
    def get_skill_analysis(cls, child_id, start_date, end_date):
        return cls.objects.filter(
            visit__child_id=child_id,
            visit__lesson_date__range=(start_date, end_date),
            mark_type__mark_category__description='Социальные навыки'
        ).aggregate(Avg('mark'))

    @classmethod
    def get_behavior_analysis(cls, child_id, start_date, end_date):
        return cls.objects.filter(
            visit__child_id=child_id,
            visit__lesson_date__range=(start_date, end_date),
            mark_type__mark_category__description='Трудное поведение'
        ).aggregate(Avg('mark'))

@receiver(pre_save, sender=Semester)
def check_add_semester(sender, instance, **kwargs):
    if Semester.objects.filter(
        models.Q(start_date__lte=instance.start_date, end_date__gte=instance.start_date) |
        models.Q(start_date__lte=instance.end_date, end_date__gte=instance.end_date)
    ).exists():
        raise ValidationError('Incorrect semester period')
    
@receiver(pre_save, sender=MarksForVisit)
def check_mark_value(sender, instance, **kwargs):
    if instance.mark > instance.mark_type.max_value:
        raise ValidationError('Too big mark has been added')
    
@receiver(pre_save, sender=Child)
def add_class_to_history(sender, instance, **kwargs):
    if instance.pk:
        old_instance = Child.objects.get(pk=instance.pk)
        if old_instance.current_group != instance.current_group:
            GroupClass.objects.filter(group_id=old_instance.current_group_id).update(
                child_id=old_instance.child_id,
                add_date=old_instance.add_to_group_date,
                leave_date=now().date()
            )
            instance.add_to_group_date = now().date()
@receiver(pre_save, sender=Worker)
def add_to_history_when_dismissial(sender, instance, **kwargs):
    if instance.dismissal_date:
        WorkerByRole.objects.filter(worker_id=instance).delete()

@receiver(pre_delete, sender=WorkerByRole)
def add_to_history_when_delete(sender, instance, **kwargs):
    LoginData.objects.filter(worker_id=instance.worker_id, level_code=instance.level_code).delete()
    WorkerHistory.objects.create(
        level_code=instance.level_code,
        worker_id=instance.worker_id,
        tensure_start_date=instance.tensure_start_date,
        tensure_end_date=now().date()
    )

@receiver(pre_save, sender=WorkerByRole)
def update_login_data(sender, instance, **kwargs):
    if instance.pk:
        old_instance = WorkerByRole.objects.get(pk=instance.pk)
        LoginData.objects.filter(worker_id=old_instance.worker_id, level_code=old_instance.level_code).update(level_code=instance.level_code)
