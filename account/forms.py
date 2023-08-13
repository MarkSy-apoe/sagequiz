from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from account.models import Account
from django.contrib.auth import login


class RegistrationFormTeacher(UserCreationForm):
	email = forms.EmailField(max_length=255, help_text=("Required. Add a valid email address"))
	first_name = forms.CharField(max_length=255, help_text=("This field is required."))
	last_name = forms.CharField(max_length=255, help_text=("This field is required."))

	class Meta:
		model = Account
		fields = ('email', 'username', 'first_name', 'last_name', 'password1', 'password2', 'is_teacher')

		def clean_email(self):
			email = self.cleaned_data['email'].lower()
			try:
				account = Account.object.get(email=email)
			except Exception as e:
				return email
			raise forms.ValidationError(f"Email {email} is already in use.")

		def clean_username(self):
			username = self.cleaned_data['username']
			try:
				account = Account.object.get(username=username)
			except Exception as e:
				return username
			raise forms.ValidationError(f"Username {username} is already in use.")

class RegistrationFormStudent(UserCreationForm):
	email = forms.EmailField(max_length=255, help_text=("Required. Add a valid email address"))
	first_name = forms.CharField(max_length=255, help_text=("This field is required."))
	last_name = forms.CharField(max_length=255, help_text=("This field is required."))

	class Meta:
		model = Account
		fields = ('email', 'username', 'first_name', 'last_name', 'password1', 'password2', 'is_student')

		def clean_email(self):
			email = self.cleaned_data['email'].lower()
			try:
				account = Account.object.get(email=email)
			except Exception as e:
				return email
			raise forms.ValidationError(f"Email {email} is already in use.")

		def clean_username(self):
			username = self.cleaned_data['username']
			try:
				account = Account.object.get(username=username)
			except Exception as e:
				return username
			raise forms.ValidationError(f"Username {username} is already in use.")
			

		

class AccountAuthenticationForm(forms.ModelForm):

	password = forms.CharField(label="Password", widget=forms.PasswordInput)

	class Meta:
		model = Account
		fields = ('email', 'password')

	def save(self, request):
		loguser = authenticate(email=self.cleaned_data['email'], password = self.cleaned_data['password'])
		if loguser:
			login(request, loguser)

			


	def clean(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']
			if not authenticate(email=email, password=password):
				raise forms.ValidationError("Invalid Login")