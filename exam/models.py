from django.db import models
from account.models import *
from django.template.defaultfilters import slugify
from django.urls import reverse

# Create your models here.
class Tag(models.Model):
	subject		= models.CharField(max_length=100, null=True)

	def __str__(self):
		return self.subject

class Difficulty(models.Model):
	diff 		= models.CharField(max_length=50, null=True)

	def __str__(self):
		return self.diff

class Exam(models.Model):
	name			= models.CharField(max_length=255, null=True)
	description		= models.TextField(blank=True, null=True)
	difficulty		= models.ForeignKey(Difficulty, on_delete = models.SET_NULL, null=True)
	tag 			= models.ForeignKey(Tag, on_delete = models.SET_NULL, null=True)
	creator			= models.ForeignKey(Teacher, on_delete = models.CASCADE, null=True)
	participated	= models.IntegerField(default=0, null=True)
	slug			= models.SlugField(null=True, unique=False)

	def __str__(self):
		return self.name

	def get_absolute_url(self):
		return reverse("exam_detail", kwargs={"slug": self.slug, "pk": self.id})

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.name)
		return super().save(*args, **kwargs)

class Question(models.Model):
	exam 		= models.ForeignKey(Exam, on_delete = models.CASCADE, null=True)
	question 	= models.CharField(max_length=200, null=True)
	op1 		= models.CharField(max_length=200, null=True)
	op2 		= models.CharField(max_length=200, null=True)
	op3 		= models.CharField(max_length=200, null=True)
	op4 		= models.CharField(max_length=200, null=True)
	ans 		= models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.question

class TheoryQuestions(models.Model):
	exam 		= models.ForeignKey(Exam, on_delete = models.CASCADE, null=True)
	question   	= models.CharField(max_length=200, null=True)
	answer		= models.CharField(max_length=200, null=True)

	def __str__(self):
		return self.exam.name + " " + self.question

class Record(models.Model):
	owner 		= models.ForeignKey(Student, on_delete=models.CASCADE, null= True)
	exam 		= models.ForeignKey(Exam, on_delete= models.CASCADE, null=True)
	teacher 	= models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
	score		= models.CharField(max_length=10, null=True)
	percentage 	= models.CharField(max_length=10, null=True)
	time_taken 	= models.CharField(max_length=10, null=True)
	difficulty  = models.CharField(max_length=10, null=True)
	date 		= models.DateTimeField(verbose_name="date taken", auto_now_add=True)



