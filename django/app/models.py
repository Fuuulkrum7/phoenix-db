from django.db import models, transaction
from django.db.models.signals import pre_save, post_save, pre_delete
from django.dispatch import receiver
from django.utils import timezone
from django.core.exceptions import ValidationError

## \class TracksType
## \brief Represents the age group for tracks.
class TracksType(models.Model):
    start_age = models.SmallIntegerField()  ## \brief Starting age of the track.
    end_age = models.SmallIntegerField()    ## \brief Ending age of the track.
    max_lessons_number = models.DecimalField(max_digits=2, decimal_places=0)  ## \brief Maximum number of lessons for the track.

    def __str__(self):
        return f'Track {self.start_age}-{self.end_age}'

## \class GroupTable
## \brief Represents a group of children.
class GroupTable(models.Model):
    track_type = models.ForeignKey(TracksType, on_delete=models.CASCADE)  ## \brief Foreign key to TracksType.

    def __str__(self):
        return f'Group {self.id}'

## \class Child
## \brief Represents a child being educated.
class Child(models.Model):
    name = models.CharField(max_length=64)    ## \brief Child's first name.
    surname = models.CharField(max_length=64) ## \brief Child's surname.
    patronymic = models.CharField(max_length=64, blank=True, null=True) ## \brief Child's patronymic.
    birthday = models.DateField() ## \brief Child's birth date.
    current_group = models.ForeignKey(GroupTable, on_delete=models.SET_NULL, null=True, blank=True) ## \brief Current group the child belongs to.
    add_to_group_date = models.DateField(auto_now_add=True) ## \brief Date the child was added to the group.
    gender = models.CharField(max_length=1) ## \brief Child's gender.

    def __str__(self):
        return f'{self.name} {self.surname}'

    class Meta:
        indexes = [
            models.Index(fields=['current_group'], name='index_child_group'),
        ]

## \class Parent
## \brief Represents a parent of a child.
class Parent(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE)  ## \brief Foreign key to Child.
    name = models.CharField(max_length=64)  ## \brief Parent's first name.
    surname = models.CharField(max_length=64) ## \brief Parent's surname.
    patronymic = models.CharField(max_length=64, blank=True, null=True) ## \brief Parent's patronymic.

    def __str__(self):
        return f'{self.name} {self.surname}'

    class Meta:
        indexes = [
            models.Index(fields=['child'], name='index_parent_f'),
        ]

## \class ParentPhones
## \brief Represents the phone numbers of parents.
class ParentPhones(models.Model):
    parent = models.ForeignKey(Parent, on_delete=models.CASCADE)  ## \brief Foreign key to Parent.
    phone_number = models.CharField(max_length=14, unique=True)  ## \brief Parent's phone number.

    def __str__(self):
        return f'{self.phone_number}'

    class Meta:
        indexes = [
            models.Index(fields=['parent', 'phone_number'], name='index_parent_phones_u'),
        ]

## \class Worker
## \brief Represents a worker.
class Worker(models.Model):
    name = models.CharField(max_length=64)  ## \brief Worker's first name.
    surname = models.CharField(max_length=64) ## \brief Worker's surname.
    patronymic = models.CharField(max_length=64, blank=True, null=True) ## \brief Worker's patronymic.
    hire_date = models.DateField() ## \brief Date the worker was hired.
    dismissal_date = models.DateField(blank=True, null=True) ## \brief Date the worker was dismissed.

    def __str__(self):
        return f'{self.name} {self.surname}'

## \class Roles
## \brief Represents the roles of users in the system.
class Roles(models.Model):
    role_name = models.CharField(max_length=32, primary_key=True) ## \brief Name of the role.
    eng_role_name = models.CharField(max_length=32) ## \brief English name of the role.
    level_code = models.CharField(max_length=1, unique=True) ## \brief Level code of the role.

    def __str__(self):
        return f'{self.role_name}'

## \class LoginData
## \brief Represents the login data for workers.
class LoginData(models.Model):
    worker_login = models.CharField(max_length=64, primary_key=True) ## \brief Worker's login.
    password = models.CharField(max_length=256) ## \brief Worker's password.
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE) ## \brief Foreign key to Worker.

    def __str__(self):
        return f'{self.worker_login}'

## \class WorkerByRole
## \brief Represents pairs of workers and their roles.
class WorkerByRole(models.Model):
    role_name = models.ForeignKey(Roles, on_delete=models.CASCADE) ## \brief Foreign key to Roles.
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE) ## \brief Foreign key to Worker.
    tensure_start_date = models.DateField(auto_now_add=True) ## \brief Start date of the tenure.

    class Meta:
        unique_together = ('role_name', 'worker')

## \class WorkerHistory
## \brief Represents previous pairs of worker and their role.
class WorkerHistory(models.Model):
    role_name = models.ForeignKey(Roles, on_delete=models.CASCADE) ## \brief Foreign key to Roles.
    worker = models.ForeignKey(Worker, on_delete=models.CASCADE) ## \brief Foreign key to Worker.
    tensure_start_date = models.DateField() ## \brief Start date of the tenure.
    tensure_end_date = models.DateField() ## \brief End date of the tenure.

## \class Course
## \brief Represents a course.
class Course(models.Model):
    course_name = models.CharField(max_length=128) ## \brief Name of the course.

    def __str__(self):
        return f'{self.course_name}'

## \class MarkCategories
## \brief Represents categories of marks.
class MarkCategories(models.Model):
    mark_category = models.CharField(max_length=32, primary_key=True) ## \brief Category of the mark.
    description = models.CharField(max_length=96) ## \brief Description of the mark category.

    def __str__(self):
        return f'{self.mark_category}'

## \class MarkTypes
## \brief Represents types of marks.
class MarkTypes(models.Model):
    description = models.CharField(max_length=512) ## \brief Description of the mark type.
    min_value = models.SmallIntegerField() ## \brief Minimum value of the mark.
    max_value = models.SmallIntegerField() ## \brief Maximum value of the mark.
    mark_category = models.ForeignKey(MarkCategories, on_delete=models.CASCADE) ## \brief Foreign key to MarkCategories.

## \class CourseByMarkTypes
## \brief Represents the association between courses and mark types.
class CourseByMarkTypes(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE) ## \brief Foreign key to Course.
    mark_type = models.ForeignKey(MarkTypes, on_delete=models.CASCADE) ## \brief Foreign key to MarkTypes.

    class Meta:
        unique_together = ('course', 'mark_type')

## \class CourseAuthors
## \brief Represents pairs of course authors.
class CourseAuthors(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE) ## \brief Foreign key to Course.
    author = models.ForeignKey(Worker, on_delete=models.CASCADE) ## \brief Foreign key to Worker.

    class Meta:
        unique_together = ('course', 'author')

## \class GroupClass
## \brief Represents a combination of group, teacher, and course.
class GroupClass(models.Model):
    group = models.ForeignKey(GroupTable, on_delete=models.CASCADE) ## \brief Foreign key to GroupTable.
    teacher = models.ForeignKey(Worker, on_delete=models.CASCADE) ## \brief Foreign key to Worker.
    course = models.ForeignKey(Course, on_delete=models.CASCADE) ## \brief Foreign key to Course.
    creation_date = models.DateField(auto_now_add=True) ## \brief Date of creation.

    class Meta:
        unique_together = ('teacher', 'group', 'course')
        indexes = [
            models.Index(fields=['teacher', 'group', 'course'], name='index_class_u'),
        ]

## \class ClassHistory
## \brief Represents previous classes where the child was.
class ClassHistory(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE) ## \brief Foreign key to Child.
    group_class = models.ForeignKey(GroupClass, on_delete=models.CASCADE) ## \brief Foreign key to GroupClass.
    add_date = models.DateField(auto_now_add=True) ## \brief Date the child was added.
    leave_date = models.DateField() ## \brief Date the child left the class.

    class Meta:
        unique_together = ('child', 'group_class')
        indexes = [
            models.Index(fields=['child', 'group_class'], name='index_class_history'),
        ]

## \class CourseComments
## \brief Represents comments about the course.
class CourseComments(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE) ## \brief Foreign key to Course.
    author = models.ForeignKey(Worker, on_delete=models.CASCADE) ## \brief Foreign key to Worker.
    description = models.CharField(max_length=512) ## \brief Description of the comment.

    class Meta:
        unique_together = ('course', 'author')

## \class ChildInfo
## \brief Represents info about the child, such as comments.
class ChildInfo(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE) ## \brief Foreign key to Child.
    author = models.ForeignKey(Worker, on_delete=models.CASCADE) ## \brief Foreign key to Worker.
    description = models.CharField(max_length=512) ## \brief Description of the info.

    class Meta:
        unique_together = ('child', 'author')

## \class ClassInfo
## \brief Represents info about the class, written by a worker.
class ClassInfo(models.Model):
    group_class = models.ForeignKey(GroupClass, on_delete=models.CASCADE) ## \brief Foreign key to GroupClass.
    author = models.ForeignKey(Worker, on_delete=models.CASCADE) ## \brief Foreign key to Worker.
    description = models.CharField(max_length=512) ## \brief Description of the info.

    class Meta:
        unique_together = ('group_class', 'author')

## \class Semester
## \brief Represents a semester.
class Semester(models.Model):
    start_date = models.DateField() ## \brief Start date of the semester.
    end_date = models.DateField() ## \brief End date of the semester.

    class Meta:
        indexes = [
            models.Index(fields=['start_date'], name='index_semester_start'),
        ]

## \class Lesson
## \brief Represents a lesson for a class.
class Lesson(models.Model):
    group_class = models.ForeignKey(GroupClass, on_delete=models.CASCADE) ## \brief Foreign key to GroupClass.
    lesson_date = models.DateTimeField() ## \brief Date of the lesson.
    duration = models.SmallIntegerField() ## \brief Duration of the lesson.
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE, null=True, blank=True) ## \brief Foreign key to Semester.

    class Meta:
        unique_together = ('group_class', 'lesson_date')
        indexes = [
            models.Index(fields=['lesson_date'], name='index_lessons_date'),
            models.Index(fields=['semester', 'group_class'], name='index_les_by_sem_and_class'),
        ]

## \class Reports
## \brief Represents reports written by a worker about a class.
class Reports(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE) ## \brief Foreign key to Child.
    group_class = models.ForeignKey(GroupClass, on_delete=models.CASCADE) ## \brief Foreign key to GroupClass.
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE) ## \brief Foreign key to Semester.
    filename = models.CharField(max_length=128) ## \brief Filename of the report.
    add_time = models.TimeField(auto_now_add=True) ## \brief Time the report was added.

    class Meta:
        unique_together = ('child', 'group_class', 'semester', 'filename')
        indexes = [
            models.Index(fields=['group_class', 'semester'], name='index_reports_by_class&sem'),
        ]

## \class VisitTypes
## \brief Represents types of class visits, such as "visited" or "not visited".
class VisitTypes(models.Model):
    visit_type_id = models.CharField(max_length=1, primary_key=True) ## \brief ID of the visit type.
    description = models.CharField(max_length=96) ## \brief Description of the visit type.

## \class Visits
## \brief Represents the fact of a visit.
class Visits(models.Model):
    child = models.ForeignKey(Child, on_delete=models.CASCADE) ## \brief Foreign key to Child.
    group_class = models.ForeignKey(GroupClass, on_delete=models.CASCADE) ## \brief Foreign key to GroupClass.
    lesson_date = models.DateTimeField() ## \brief Date of the lesson.
    visit_type = models.ForeignKey(VisitTypes, on_delete=models.CASCADE) ## \brief Foreign key to VisitTypes.

    class Meta:
        unique_together = ('child', 'group_class', 'lesson_date')
        indexes = [
            models.Index(fields=['child', 'group_class', 'lesson_date'], name='index_visits_u'),
            models.Index(fields=['group_class', 'lesson_date'], name='index_visits_by_lesson'),
        ]

## \class MarksForVisit
## \brief Represents marks given for a visit.
class MarksForVisit(models.Model):
    visit = models.ForeignKey(Visits, on_delete=models.CASCADE) ## \brief Foreign key to Visits.
    mark_type = models.ForeignKey(MarkTypes, on_delete=models.CASCADE) ## \brief Foreign key to MarkTypes.
    mark = models.DecimalField(max_digits=3, decimal_places=1) ## \brief The mark given.

    class Meta:
        indexes = [
            models.Index(fields=['mark'], name='index_marks_value'),
        ]

    def __str__(self):
        return f'{self.mark}'
   
# Trigger function equivalents

## \brief Checks the semester for the lesson.
## \details If the semester is not set, it sets the correct semester based on the lesson date. Raises an exception if the semester is invalid.
## \param sender The model class.
## \param instance The instance being saved.
## \param kwargs Additional keyword arguments.
@receiver(pre_save, sender=Lesson)
def check_semester_in_lesson(sender, instance, **kwargs):
    if instance.semester is None:
        semester = Semester.objects.filter(start_date__lte=instance.lesson_date.date(),
                                            end_date__gte=instance.lesson_date.date()).first()
        if semester:
            instance.semester = semester
        else:
            raise ValidationError('Not correct lesson date')
    else:
        if not Semester.objects.filter(pk=instance.semester_id, start_date__lte=instance.lesson_date.date(),
                                       end_date__gte=instance.lesson_date.date()).exists():
            raise ValidationError('Not correct semester id')

## \brief Checks for overlapping lessons before adding a new lesson.
## \details Ensures that no existing lessons overlap with the new lesson's start time.
## \param sender The model class.
## \param instance The instance being saved.
## \param kwargs Additional keyword arguments.
@receiver(pre_save, sender=Lesson)
def check_add_lesson(sender, instance, **kwargs):
    if Lesson.objects.filter(
            lesson_date__lte=instance.lesson_date,
            lesson_date__gte=instance.lesson_date,
            group_class=instance.group_class
    ).exists():
        raise ValidationError('Incorrect lesson start time')

## \brief Checks for overlapping semesters before adding a new semester.
## \details Ensures that the new semester's period does not overlap with existing semesters.
## \param sender The model class.
## \param instance The instance being saved.
## \param kwargs Additional keyword arguments.
@receiver(pre_save, sender=Semester)
def check_add_semester(sender, instance, **kwargs):
    if Semester.objects.filter(
            start_date__lte=instance.start_date,
            end_date__gte=instance.start_date
    ).exists():
        raise ValidationError('Incorrect semester period')

## \brief Validates the mark value before saving.
## \details Ensures that the mark value does not exceed the maximum allowed value.
## \param sender The model class.
## \param instance The instance being saved.
## \param kwargs Additional keyword arguments.
@receiver(pre_save, sender=MarksForVisit)
def check_mark_value(sender, instance, **kwargs):
    if instance.mark > instance.mark_type.max_value:
        raise ValidationError('Too big mark has been added')

## \brief Adds class history when a child changes groups.
## \details Records the class history if the child's current group changes.
## \param sender The model class.
## \param instance The instance being saved.
## \param kwargs Additional keyword arguments.
@receiver(pre_save, sender=Child)
def add_class_to_history(sender, instance, **kwargs):
    if instance.pk:
        original = Child.objects.get(pk=instance.pk)
        if original.current_group_id != instance.current_group_id:
            GroupClass.objects.create(
                child=instance,
                class_id=original.current_group_id,
                add_date=original.add_to_group_date,
                leave_date=models.functions.Now()
            )
            instance.add_to_group_date = models.functions.Now()

## \brief Handles worker dismissal updates.
## \details Deletes the worker's role if the dismissal date is set.
## \param sender The model class.
## \param instance The instance being saved.
## \param kwargs Additional keyword arguments.
@receiver(pre_save, sender=Worker)
def add_to_history_when_dismissial(sender, instance, **kwargs):
    if instance.dismissal_date:
        WorkerByRole.objects.filter(worker=instance).delete()

## \brief Adds worker history when a role is deleted.
## \details Records the worker's role history when the role is deleted.
## \param sender The model class.
## \param instance The instance being deleted.
## \param kwargs Additional keyword arguments.
@receiver(pre_delete, sender=WorkerByRole)
def add_to_history_when_delete(sender, instance, **kwargs):
    WorkerHistory.objects.create(
        role_name=instance.role_name,
        worker=instance.worker,
        tensure_start_date=instance.tensure_start_date,
        tensure_end_date=models.functions.Now()
    )