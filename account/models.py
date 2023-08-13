from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.template.defaultfilters import slugify
from django.urls import reverse

# Create your models here.
class MyAccountManager(BaseUserManager):

	def create_user(self, email, username, first_name, last_name, password=None):
		if not email:
			raise ValueError("Users must have an email address.")
		if not username:
			raise ValueError("Users must have an username.")
		if not first_name:
			raise ValueError("Users must have an first_name.")
		if not last_name:
			raise ValueError("Users must have an last_name.")

		user = self.model(
			email=self.normalize_email(email),
			username=username,
			first_name=first_name,
			last_name=last_name,
		)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, username, first_name, last_name, password):
		user = self.create_user(
			email=email,
			username=username,
			first_name=first_name,
			last_name=last_name,
			password=password,
		)

		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.is_approved = True

		user.save(using=self._db)
		return user


class Account(AbstractBaseUser):
	email 			= models.EmailField(verbose_name="email", max_length=60, unique=True)
	first_name 		= models.CharField(max_length=30, null=True)
	last_name 		= models.CharField(max_length=30, null=True)
	username 		= models.CharField(max_length=30, unique=True)
	date_joined 	= models.DateTimeField(verbose_name="date joined", auto_now_add=True)
	last_login 		= models.DateTimeField(verbose_name="last_login", auto_now=True)
	is_admin 		= models.BooleanField(default=False)
	is_active 		= models.BooleanField(default=True)
	is_staff 		= models.BooleanField(default=False)
	is_superuser 	= models.BooleanField(default=False)
	is_teacher 		= models.BooleanField(default=False)
	is_student 		= models.BooleanField(default=False)
	is_approved		= models.BooleanField(default=False)

	objects = MyAccountManager()

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

	def __str__(self):
		return self.username

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return True

class Teacher(models.Model):
	user 	= models.OneToOneField(Account, on_delete=models.CASCADE, null=True)
	bio     = models.CharField(max_length=255, null=True)
	examsmade = models.IntegerField(default=0, null=True)
	slug	= models.SlugField(null=True, unique=True)
	
	def __str__(self):
		return self.user.username

	def get_absolute_url(self):
		return reverse("userteacher_detail", kwargs={"slug": self.slug})

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.user.username)
		return super().save(*args, **kwargs)

class Student(models.Model):
	user 	= models.OneToOneField(Account, on_delete=models.CASCADE, null=True)
	examtaken = models.IntegerField(default=0, null=True)
	exampassed = models.IntegerField(default=0, null=True)
	bio     = models.CharField(max_length=255, null=True, blank=True)
	slug	= models.SlugField(null=True, unique=True)
	
	def __str__(self):
		return self.user.username

	def get_absolute_url(self):
		return reverse("userstudent_detail", kwargs={"slug": self.slug})

	def save(self, *args, **kwargs):
		if not self.slug:
			self.slug = slugify(self.user.username)
		return super().save(*args, **kwargs)