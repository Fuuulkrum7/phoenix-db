from django.db import models
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver
from django.core.exceptions import ValidationError
from django.utils.timezone import now
from django.db.models import Avg

## \class TrackType
## \brief Represents the types of tracks for different age groups.
class TrackType(models.Model):
    track_type_id = models.AutoField(primary_key=True)
    start_age = models.SmallIntegerField(null=False)
    end_age = models.SmallIntegerField(null=False)
    max_lessons_number = models.DecimalField(max_digits=1, decimal_places=0, null=False)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(start_age__gt=0), name='check_start_age_gt_0'),
            models.CheckConstraint(check=models.Q(end_age__gte=models.F('start_age')), name='check_end_age_gte_start_age'),
            models.CheckConstraint(check=models.Q(max_lessons_number__gt=0), name='check_max_lessons_number_gt_0')
        ]

## \class Group
## \brief Represents a group of children.
class Group(models.Model):
    group_id = models.AutoField(primary_key=True)
    group_name = models.CharField(max_length=64, null=False)
    track_type = models.ForeignKey(TrackType, on_delete=models.CASCADE)


## \class Child
## \brief Represents a child enrolled in the system.
class Child(models.Model):
    child_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, null=False)
    surname = models.CharField(max_length=64, null=False)
    patronymic = models.CharField(max_length=64, blank=True, null=True)
    birthday = models.DateField(null=False)
    current_group = models.ForeignKey(Group, on_delete=models.CASCADE, null=True)
    add_to_group_date = models.DateField(auto_now_add=True, null=True)
    gender = models.CharField(max_length=1, null=False)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(birthday__lt=models.functions.Now()), name='check_birthday_lt_current_date')
        ]

## \class Parent
## \brief Represents a parent of a child.
class Parent(models.Model):
    parent_id = models.AutoField(primary_key=True)
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    name = models.CharField(max_length=64, null=False)
    surname = models.CharField(max_length=64, null=False)
    patronymic = models.CharField(max_length=64, blank=True, null=True)

## \class ParentPhone
## \brief Represents the phone number of a parent.
class ParentPhone(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=14, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['parent', 'phone_number'], name='unique_parent_phone')
        ]

## \class Worker
## \brief Represents a worker in the system.
class Worker(models.Model):
    worker_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=64, null=False)
    surname = models.CharField(max_length=64, null=False)
    patronymic = models.CharField(max_length=64, blank=True, null=True)
    hire_date = models.DateField(null=False)
    dismissal_date = models.DateField(blank=True, null=True)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(hire_date__lte=models.functions.Now()), name='check_hire_date_le_current_date'),
            models.CheckConstraint(check=models.Q(dismissal_date__gt=models.F('hire_date')), name='check_dismissal_date_gt_hire_date')
        ]

## \class Role
## \brief Represents a role in the system.
class Role(models.Model):
    level_code = models.CharField(max_length=1, primary_key=True)
    role_name = models.CharField(max_length=32, unique=True, null=False)
    eng_role_name = models.CharField(max_length=32, null=False)

## \class WorkerByRole
## \brief Represents the association of a worker with a role.
class WorkerByRole(models.Model):
    level_code = models.ForeignKey(Role, on_delete=models.CASCADE)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    tensure_start_date = models.DateField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(tensure_start_date__lte=models.functions.Now()), name='check_tens_st_date_le_curr_date'),
            models.UniqueConstraint(fields=['level_code', 'worker'], name='primary_worker_role')
        ]

## \class LoginData
## \brief Represents login data for a worker.
class LoginData(models.Model):
    worker_login = models.CharField(max_length=64, primary_key=True)
    password = models.CharField(max_length=256, null=False)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)

## \class WorkerHistory
## \brief Represents the history of a worker's roles.
class WorkerHistory(models.Model):
    level_code = models.ForeignKey(Role, on_delete=models.CASCADE)
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE)
    tensure_start_date = models.DateField(null=False)
    tensure_end_date = models.DateField(null=False)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(tensure_start_date__lte=models.functions.Now()), name='check_tensure_start_date_le_current_date'),
            models.CheckConstraint(check=models.Q(tensure_end_date__gte=models.F('tensure_start_date')), name='check_tensure_end_date_ge_tensure_start_date')
        ]

## \class Course
## \brief Represents a course.
class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_name = models.CharField(max_length=128, null=False)

## \class MarkCategory
## \brief Represents a category of marks.
class MarkCategory(models.Model):
    mark_category = models.CharField(max_length=32, primary_key=True)
    description = models.CharField(max_length=96, null=False)

## \class MarkType
## \brief Represents a type of mark.
class MarkType(models.Model):
    mark_type_id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=512, null=False)
    min_value = models.SmallIntegerField(null=False)
    max_value = models.SmallIntegerField(null=False)
    mark_category = models.ForeignKey(MarkCategory, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(min_value__gte=0), name='check_min_value_gte_0'),
            models.CheckConstraint(check=models.Q(max_value__gt=models.F('min_value')), name='check_max_value_gt_min_value')
        ]

## \class CourseByMarkType
## \brief Represents the association of a course with mark types.
class CourseByMarkType(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    mark_type = models.ForeignKey(MarkType, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['course', 'mark_type'], name='primary_course_by_mark')
        ]

## \class CourseAuthor
## \brief Represents the authorship of a course.
class CourseAuthor(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    author = models.ForeignKey(Worker, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['course', 'author'], name='primary_course_by_author')
        ]

## \class GroupClass
## \brief Represents a class within a group, associated with a teacher and a course.
class GroupClass(models.Model):
    class_id = models.AutoField(primary_key=True)
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Worker, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    creation_date = models.DateField(null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['teacher', 'group', 'course'], name='unique_class')
        ]

## \class ClassHistory
## \brief Represents the history of classes a child has been in.
class ClassHistory(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    class_instance = models.ForeignKey(GroupClass, on_delete=models.CASCADE)
    add_date = models.DateField(null=False)
    leave_date = models.DateField(null=False)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(add_date__lte=models.functions.Now()), name='check_add_date_le_current_date'),
            models.CheckConstraint(check=models.Q(leave_date__gte=models.F('add_date')), name='check_leave_date_ge_add_date'),
            models.UniqueConstraint(fields=['child', 'class_instance'], name='primary_class_history')
        ]

## \class CourseComment
## \brief Represents comments about a course.
class CourseComment(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    author = models.ForeignKey(Worker, on_delete=models.CASCADE)
    description = models.CharField(max_length=512, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['course', 'author'], name='primary_course_comments')
        ]

## \class ChildInfo
## \brief Represents information about a child, such as comments.
class ChildInfo(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    author = models.ForeignKey(Worker, on_delete=models.CASCADE)
    description = models.CharField(max_length=512, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['child', 'author'], name='primary_child_info')
        ]

## \class ClassInfo
## \brief Represents information about a class, written by a worker.
class ClassInfo(models.Model):
    class_instance = models.ForeignKey(GroupClass, on_delete=models.CASCADE)
    author = models.ForeignKey(Worker, on_delete=models.CASCADE)
    description = models.CharField(max_length=512, null=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['class_instance', 'author'], name='primary_class_info')
        ]

## \class Semester
## \brief Represents a semester with a start and end date.
class Semester(models.Model):
    semester_id = models.AutoField(primary_key=True)
    start_date = models.DateField(null=False)
    end_date = models.DateField(null=False)

    class Meta:
        constraints = [
            models.CheckConstraint(check=models.Q(end_date__gt=models.F('start_date')), name='check_end_date_gt_start_date')
        ]

## \class Lesson
## \brief Represents a lesson for a class within a semester.
class Lesson(models.Model):
    class_instance = models.ForeignKey(GroupClass, on_delete=models.CASCADE)
    lesson_date = models.DateTimeField(null=False)
    duration = models.SmallIntegerField(null=False)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, blank=True, null=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['class_instance', 'lesson_date'], name='primary_lesson')
        ]

## \class Report
## \brief Represents a report written by a worker about a class.
class Report(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    class_instance = models.ForeignKey(GroupClass, on_delete=models.CASCADE)
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    filename = models.CharField(max_length=128, null=False)
    add_time = models.TimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['child', 'class_instance', 'semester', 'filename'], name='primary_reports')
        ]

## \class Visit
## \brief Represents a visit record for a child to a lesson.
class Visits(models.Model):
    visit_id = models.AutoField(primary_key=True)
    child = models.ForeignKey(Child, on_delete=models.CASCADE)
    group_class = models.ForeignKey(GroupClass, on_delete=models.CASCADE)
    lesson_date = models.DateTimeField(null=False)
    description = models.CharField(max_length=96, null=True)
    visited = models.BooleanField(default=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['child', 'group_class', 'lesson_date'], name='unique_visit')
        ]
    def clean(self):
        super().clean()
        if not Lesson.objects.filter(class_instance=self.group_class, lesson_date=self.lesson_date).exists():
            raise ValidationError('Invalid combination of class_instance and lesson_date.')

@receiver(pre_save, sender=Visits)
def validate_visit(sender, instance, **kwargs):
    instance.clean()

## \class GroupCreators
## \brief Represents the association between a group and its curator.
class GroupCreators(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    curator = models.ForeignKey(Worker, on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['group', 'curator'], name='primary_group_by_creator')
        ]

## \class MarksForVisit
## \brief Represents marks given for a visit.
class MarksForVisit(models.Model):
    visit = models.ForeignKey(Visits, on_delete=models.CASCADE) ## \brief Foreign key to Visits.
    mark_type = models.ForeignKey(MarkType, on_delete=models.CASCADE) ## \brief Foreign key to MarkTypes.
    mark = models.DecimalField(max_digits=3, decimal_places=1) ## \brief The mark given.

    class Meta:
        indexes = [
            models.Index(fields=['mark'], name='index_marks_value'),
        ]
    
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

@receiver(pre_save, sender=Lesson)
def check_semester_in_lesson(sender, instance, **kwargs):
    if instance.semester is None:
        try:
            instance.semester = Semester.objects.get(start_date__lte=instance.lesson_date, end_date__gte=instance.lesson_date)
        except Semester.DoesNotExist:
            raise ValidationError('Not correct lesson date')
    else:
        if not Semester.objects.filter(pk=instance.semester.pk, start_date__lte=instance.lesson_date, end_date__gte=instance.lesson_date).exists():
            raise ValidationError('Not correct semester id')

@receiver(pre_save, sender=Lesson)
def check_add_lesson(sender, instance, **kwargs):
    if Lesson.objects.filter(
        models.Q(lesson_date__lte=instance.lesson_date, lesson_date__gte=instance.lesson_date) |
        models.Q(lesson_date__lte=instance.lesson_date + instance.duration, lesson_date__gte=instance.lesson_date)
    ).exists():
        raise ValidationError('Incorrect lesson start time')
    
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
        WorkerByRole.objects.filter(worker=instance).delete()

@receiver(pre_delete, sender=WorkerByRole)
def add_to_history_when_delete(sender, instance, **kwargs):
    LoginData.objects.filter(worker_id=instance.worker_id, level_code=instance.level_code).delete()
    WorkerHistory.objects.create(
        level_code=instance.level_code,
        worker=instance.worker,
        tensure_start_date=instance.tensure_start_date,
        tensure_end_date=now().date()
    )

@receiver(pre_save, sender=WorkerByRole)
def update_login_data(sender, instance, **kwargs):
    if instance.pk:
        old_instance = WorkerByRole.objects.get(pk=instance.pk)
        LoginData.objects.filter(worker_id=old_instance.worker_id, level_code=old_instance.level_code).update(level_code=instance.level_code)