from django.contrib import admin
from exam.models import *
# Register your models here.

admin.site.register(Tag)
admin.site.register(Difficulty)
admin.site.register(Exam)
admin.site.register(Question)
admin.site.register(TheoryQuestions)
admin.site.register(Record)