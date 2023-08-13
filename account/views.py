from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views import View
from django.contrib.auth import login, authenticate, logout
from account.models import *
from exam.models import *
from exam.forms import *
from account.forms import RegistrationFormTeacher, RegistrationFormStudent, AccountAuthenticationForm
from django.shortcuts import(get_object_or_404, render, HttpResponseRedirect)

# Create your views here.
def edit_bio(request):
	user = request.user
	context={'user':user}

	if user.is_authenticated:
		if user.is_teacher:
			teacher = Teacher.objects.get(user=user)
			if request.POST:
				teacher.bio = request.POST.get("bio")
				teacher.save()
				return redirect("profile")
		elif user.is_student:
			student = Student.objects.get(user=user)
			if request.POST:
				student.bio = request.POST.get("bio")
				student.save()
				return redirect("profile")
		else:
			return redirect("index")
	else:
		return redirect("index")


	return render(request, "edit_profile.html", context)


def exam_delete(request, slug, pk):
	user = request.user
	exam = Exam.objects.get(id=pk)
	context={'user': user}

	obj = get_object_or_404(Exam, slug=slug, id=pk)

	if user.is_authenticated:
		if exam.creator.user == user:
			if request.method == "POST":
				obj.delete()

				return HttpResponseRedirect("/")
		else:
			return redirect("index")
	else:
			return redirect("index")

	return render(request, "delete_exam.html", context)

def userteacher_detail(request, slug):
	user = request.user
	teacher = Teacher.objects.get(slug=slug)
	context={'user':user}
	context['teacher']=teacher

	if teacher.examsmade <= 10:
		level = "Teacher"
	elif teacher.examsmade <= 20:
		level = "Enlightened one"
	elif teacher.examsmade <= 50:
		level = "Father to many"
	elif teacher.examsmade <= 100:
		level = "Relentless educator"
	elif teacher.examsmade <= 150:
		level = "Sensei"
	elif teacher.examsmade <= 200:
		level = "Master"
	elif teacher.examsmade <= 300:
		level = "Professor"
	elif teacher.examsmade <= 400:
		level = "Professor ii"
	elif teacher.examsmade <= 700:
		level = "Professor iii"
	elif teacher.examsmade <= 900:
		level = "Oracle"
	elif teacher.examsmade <= 1500:
		level = "Unstoppable"
	else:
		level = "One above all, Master of education"

	context['level']=level

	return render(request, "teacher_profile.html", context)

def userstudent_detail(request, slug):
	user = request.user
	studentin = Student.objects.get(slug=slug)
	context={'user':user}
	context['student']=studentin

	if studentin.exampassed <= 10:
		level = "Book worm"
	elif studentin.exampassed <= 20:
		level = "Smarty pants"
	elif studentin.exampassed <= 50:
		level = "Book lover"
	elif studentin.exampassed <= 100:
		level = "Genius"
	elif studentin.exampassed <= 150:
		level = "Einstein"
	elif studentin.exampassed <= 200:
		level = "Tha next big thing"
	elif studentin.exampassed <= 300:
		level = "Super human intelligence"
	elif studentin.exampassed <= 400:
		level = "Genius Alien"
	elif studentin.exampassed <= 550:
		level = "Insanely Smart"
	elif studentin.exampassed <= 700:
		level = "god tier smarty pants"
	elif studentin.exampassed <= 900:
		level = "Universal intelligence"
	elif studentin.exampassed <= 1500:
		level = "God of intelligence"
	else:
		level = "Oracle- He's above intelligence"

	context['level']=level


	return render(request, "student_profile.html", context)

def exam_detail(request, slug, pk):
	user = request.user
	touse = Exam.objects.get(id=pk)
	context={'user':user}
	context["exam"]=Exam.objects.get(slug=slug, id=pk)
	context['question']= Question.objects.filter(exam=Exam.objects.get(id=pk))


	

	if request.POST:
		score = 0
		wrong = 0
		correct = 0
		total = 0
		questions = Question.objects.filter(exam=touse)
		for q in questions:
			total += 1
			if q.ans == request.POST.get(f"{q.question}{q.id}"):
				score += 10
				correct += 1
			else:
				wrong += 1
		percentage = score/(total*10) *100

		touse.participated = touse.participated + 1
		touse.save()

		if user.is_authenticated:
			if user.is_teacher:
				teacher = Teacher.objects.get(user=user)
				context['teacher'] = teacher

			if user.is_student:
				newrecord = Record(owner=Student.objects.get(user=user), exam=touse, teacher=touse.creator, score=score, percentage=percentage, time_taken=request.POST.get('timer'), difficulty=touse.difficulty)
				newrecord.save()
				statscount = Student.objects.get(user=user)
				statscount.examtaken = statscount.examtaken + 1
				statscount.save()
				if percentage >= 50:
					statscount.exampassed = statscount.exampassed + 1
					statscount.save()

		context={
			"score" : score,
			"correct" : correct,
			"wrong" : wrong,
			"percentage" : percentage,
			"total" : total,
			"time": request.POST.get('timer')
		}
		return render(request, "results.html", context)


	return render(request, "exam.html", context)

def add_question(request, slug, pk):
	user=request.user
	editingexam = Exam.objects.get(slug=slug, id=pk)
	#own = editingexam.creator.user
	added = False
	
	context={'user':user, 'added':added}
	context['exam']=Exam.objects.get(slug=slug, id=pk)

	if request.POST:
		newquestion = Question(exam=Exam.objects.get(slug=slug, id=pk), question=request.POST.get("question"), op1=request.POST.get("op1"), op2=request.POST.get("op2"), op3=request.POST.get("op3"), op4=request.POST.get("op4"), ans=request.POST.get("ans"))
		newquestion.save()
		delquest = Question.objects.filter(exam=Exam.objects.get(slug=slug, id=pk))
		if delquest[0].question == "What is 2+2?(default question)":
			delit = Question.objects.get(exam=Exam.objects.get(slug=slug, id=pk), question="What is 2+2?(default question)")
			delit.delete()

		added = True
		context['added']=added
		return render(request, "add_question.html", context)

	if user.is_authenticated == False:
		return redirect("index")

	if user.is_authenticated:
		if user.is_teacher == False:
			return redirect("index")

	if editingexam.creator.user != user:
		return redirect("index")





	return render(request, "add_question.html", context)


def create_exam(request):
	user=request.user
	done = False

	easy = Difficulty.objects.get(diff="Easy")
	medium = Difficulty.objects.get(diff="Medium")
	hard = Difficulty.objects.get(diff="Hard")

	mathematics = Tag.objects.get(subject="Mathematics")
	english = Tag.objects.get(subject="English")
	chemistry = Tag.objects.get(subject="Chemistry")
	physics = Tag.objects.get(subject="Physics")
	biology = Tag.objects.get(subject="Biology")
	government = Tag.objects.get(subject="Government")
	history = Tag.objects.get(subject="History")
	agriculture = Tag.objects.get(subject="Agriculture")
	civic = Tag.objects.get(subject="Civic Education")
	literature = Tag.objects.get(subject="Literature")
	programming = Tag.objects.get(subject="Programming")
	cybersec = Tag.objects.get(subject="Cyber Security")

	context = {
		'user':user,
		'english':english,
		'chemistry':chemistry,
		'physics':physics,
		'biology':biology,
		'government':government,
		'history':history,
		'mathematics':mathematics,
		'agriculture':agriculture,
		'civic':civic,
		'literature':literature,
		'programming':programming,
		'cybersec':cybersec,
		'easy':easy,
		'medium':medium,
		'hard':hard,
		'done':done,
	}


	if request.POST:
		difficulty = Difficulty.objects.get(diff=request.POST.get("difficulty"))
		tag = Tag.objects.get(subject=request.POST.get("tag"))
		newexam = Exam(name=request.POST.get("name"), description=request.POST.get("description"), difficulty=difficulty, tag=tag, creator=Teacher.objects.get(user=user))
		newexam.save()
		defaultquest = Question(question="What is 2+2?(default question)", op1="2", op2="22", op3="4", op4="10", ans="option3", exam=newexam)
		defaultquest.save()
		teacher = Teacher.objects.get(user=user)
		teacher.examsmade = teacher.examsmade + 1
		teacher.save()
		done = True
		url = newexam
		context['url']=url
		context['done']=done
		return render(request, "create_exam.html", context)	

	if user.is_authenticated == False:
		return redirect("index")

	if user.is_authenticated:
		if user.is_teacher == False:
			return redirect("index")


	return render(request, "create_exam.html", context)

def test_library(request):
	user = request.user


	mathematics = Exam.objects.filter(tag=Tag.objects.get(subject="Mathematics"))
	english = Exam.objects.filter(tag=Tag.objects.get(subject="English"))
	chemistry = Exam.objects.filter(tag=Tag.objects.get(subject="Chemistry"))
	physics = Exam.objects.filter(tag=Tag.objects.get(subject="Physics"))
	biology = Exam.objects.filter(tag=Tag.objects.get(subject="Biology"))
	government = Exam.objects.filter(tag=Tag.objects.get(subject="Government"))
	history = Exam.objects.filter(tag=Tag.objects.get(subject="History"))
	agriculture = Exam.objects.filter(tag=Tag.objects.get(subject="Agriculture"))
	civic = Exam.objects.filter(tag=Tag.objects.get(subject="Civic Education"))
	literature = Exam.objects.filter(tag=Tag.objects.get(subject="Literature"))
	programming = Exam.objects.filter(tag=Tag.objects.get(subject="Programming"))
	cybersec = Exam.objects.filter(tag=Tag.objects.get(subject="Cyber Security"))

	context = {
		'user':user,
		'english':english,
		'mathematics':mathematics,
		'chemistry':chemistry,
		'physics':physics,
		'biology':biology,
		'government':government,
		'history':history,
		'agriculture':agriculture,
		'civic':civic,
		'literature':literature,
		'programming':programming,
		'cybersec':cybersec,
	}

	return render(request, 'test_library.html', context)

def records(request):
	user = request.user
	context = {'user': user}

	if user.is_student:
		student=Student.objects.get(user=user)
		record = Record.objects.filter(owner=student)
		context['student']=student
		context['record']=record
	else:
		return redirect("index")

	return render(request, 'student_records.html', context)

def profile(request):
	user = request.user
	context = {'user': user}


	if user.is_authenticated:
		if user.is_student:
			context['student']=Student.objects.get(user=user)
			student = Student.objects.get(user=user)
			if request.method == "POST":
				student.delete()
				user.delete()
				return redirect("index")
		else:
			context['teacher']=Teacher.objects.get(user=user)
			teacher = Teacher.objects.get(user=user)
			if request.method == "POST":
				teacher.delete()
				user.delete()
				return redirect("index")
	else:
		return redirect("index")

	return render(request, 'profile.html', context)

def index(request):
	user = request.user
	context = {'user': user}




	if user.is_authenticated:
		if user.is_student:
			studentin = Student.objects.get(user=user)
			context['student']= studentin
			context['record']= Record.objects.filter(owner=studentin)
			if studentin.exampassed <= 10:
				level = "Book worm"
			elif studentin.exampassed <= 20:
				level = "Smarty pants"
			elif studentin.exampassed <= 50:
				level = "Book lover"
			elif studentin.exampassed <= 100:
				level = "Genius"
			elif studentin.exampassed <= 150:
				level = "Einstein"
			elif studentin.exampassed <= 200:
				level = "Tha next big thing"
			elif studentin.exampassed <= 300:
				level = "Super human intelligence"
			elif studentin.exampassed <= 400:
				level = "Genius Alien"
			elif studentin.exampassed <= 550:
				level = "Insanely Smart"
			elif studentin.exampassed <= 700:
				level = "god tier smarty pants"
			elif studentin.exampassed <= 900:
				level = "Universal intelligence"
			elif studentin.exampassed <= 1500:
				level = "God of intelligence"
			else:
				level = "Oracle- He's above intelligence"

			context['level']=level


		if user.is_teacher:
			teacher = Teacher.objects.get(user=user)
			context['teacher']= teacher
			context['myexam']=Exam.objects.filter(creator=Teacher.objects.get(user=user))
			if teacher.examsmade <= 10:
				level = "Teacher"
			elif teacher.examsmade <= 20:
				level = "Enlightened one"
			elif teacher.examsmade <= 50:
				level = "Father to many"
			elif teacher.examsmade <= 100:
				level = "Relentless educator"
			elif teacher.examsmade <= 150:
				level = "Sensei"
			elif teacher.examsmade <= 200:
				level = "Master"
			elif teacher.examsmade <= 300:
				level = "Professor"
			elif teacher.examsmade <= 400:
				level = "Professor ii"
			elif teacher.examsmade <= 700:
				level = "Professor iii"
			elif teacher.examsmade <= 900:
				level = "Oracle"
			elif teacher.examsmade <= 1500:
				level = "Unstoppable"
			else:
				level = "One above all, Master of education"

			context['level']=level

	context["exam"]=Exam.objects.all()
	
	return render(request, 'index.html', context)

def logout_view(request):
	logout(request)
	return redirect("index")

def login(request, *args, **kwargs):
	context = {}
	user = request.user
	if user.is_authenticated:
		return redirect("index")

	
	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			
			form.save(request)
			return redirect("index")

		else:
			context['login_form'] = form

	return render(request, 'login.html', context)


def get_redirect_if_exists(request):
	redirect = None
	if request.GET:
		if request.GET.get("next"):
			redirect = str(request.GET.get("next"))

	return redirect

def registerTea(request, *args, **kwargs):
	user = request.user
	if user.is_authenticated:
		return redirect("index")
	context ={}

	if request.POST:
		form = RegistrationFormTeacher(request.POST)
		if form.is_valid():
			Teacher.objects.create(user=form.save())
			form.save()
			destination = get_redirect_if_exists(request)
			done = True
			context['done'] = done
			return render(request, 'index.html', context)
		else:
			context['registration_form'] = form

	return render(request, 'teacher_register.html', context)


def registerStudent(request, *args, **kwargs):
	user = request.user
	if user.is_authenticated:
		return redirect("index")
	context ={}

	if request.POST:
		form = RegistrationFormStudent(request.POST)
		if form.is_valid():
			Student.objects.create(user=form.save())
			form.save()
			destination = get_redirect_if_exists(request)
			if destination:
				return redirect(destination)
			done = True
			context['done'] = done
			return render(request, 'index.html', context)
		else:
			context['registration_form'] = form

	return render(request, 'student_register.html', context)