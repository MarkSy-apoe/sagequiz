from django import forms
from exam.models import *

class AddQuestion(forms.ModelForm):
	class Meta:
		model = Question
		fields = ('question', 'op1', 'op2', 'op3', 'op4', 'ans')

		