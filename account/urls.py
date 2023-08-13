from django.contrib import admin
from . import views
from django.urls import path

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name="logout"),
    path('join/', views.registerStudent, name='registerStudent'),
    path('join-as-teacher/', views.registerTea, name='registerTea'),
    path('profile/', views.profile, name="profile"),
    path('record/', views.records, name="record"),
    path('library/', views.test_library, name="library"),
    path('create-exam/', views.create_exam, name="createexam"),
    path('<slug:slug>.<int:pk>/', views.exam_detail, name="exam_detail"),
    path('<slug:slug>.<int:pk>/delete', views.exam_delete, name="exam_delete"),
    path('<slug:slug>.<int:pk>/add-question', views.add_question, name="add_question"),
    path('student/<slug:slug>/', views.userstudent_detail, name="userstudent_detail"),
    path('teacher/<slug:slug>/', views.userteacher_detail, name="userteacher_detail"),
    path('edit-bio/', views.edit_bio, name="edit_bio")
]