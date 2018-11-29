#from django.urls import path
from django.conf.urls import url,include
from django.views.generic import TemplateView

from . import views

urlpatterns = [
    url(r'^$', views.home , name='index'),
    url(r'^student_profile/$', views.student_profile, name='student_profile'),
    url(r'^company_profile/', views.company_profile, name='company_profile'),
    url(r'^student_profile/register/', views.register, name='register'),
    url(r'^company/', views.company, name='company'),
    url(r'^jobinfo/', views.jobinfo, name='jobinfo'),
    url(r'^logout/', views.logoutfn, name='logout'),

]