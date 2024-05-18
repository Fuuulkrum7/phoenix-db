# app/admin.py
from django.contrib import admin
from .models import (
    TracksType, GroupTable, Child, Parent, ParentPhones, Worker, Roles, LoginData, WorkerByRole,
    WorkerHistory, Course, MarkCategories, MarkTypes, CourseByMarkTypes, CourseAuthors, GroupClass,
    ClassHistory, CourseComments, ChildInfo, ClassInfo, Semester, Lesson, Reports, VisitTypes, Visits, MarksForVisit
)

admin.site.register(TracksType)
admin.site.register(GroupTable)
admin.site.register(Child)
admin.site.register(Parent)
admin.site.register(ParentPhones)
admin.site.register(Worker)
admin.site.register(Roles)
admin.site.register(LoginData)
admin.site.register(WorkerByRole)
admin.site.register(WorkerHistory)
admin.site.register(Course)
admin.site.register(MarkCategories)
admin.site.register(MarkTypes)
admin.site.register(CourseByMarkTypes)
admin.site.register(CourseAuthors)
admin.site.register(GroupClass)
admin.site.register(ClassHistory)
admin.site.register(CourseComments)
admin.site.register(ChildInfo)
admin.site.register(ClassInfo)
admin.site.register(Semester)
admin.site.register(Lesson)
admin.site.register(Reports)
admin.site.register(VisitTypes)
admin.site.register(Visits)
admin.site.register(MarksForVisit)
