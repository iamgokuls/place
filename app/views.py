# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from _mysql import connection

from django.contrib.auth.models import User
from django.db import connection
from django.http import JsonResponse

from .models import *
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, HttpResponse, redirect

from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def home(request):
    if(request.method=="GET"):
        return render(request,'index.html',{})

    else:
        #return HttpResponse("logging in..........")
        username=request.POST.get('username')
        password=request.POST.get('password')
        type=request.POST.get('type')
        print(type)

        #return HttpResponse(username+password)
        u=authenticate(username=username, password=password)
        if u:
            login(request,u)
            if(type=='1'):
                return redirect('student_profile/')
            else:
                return redirect('company_profile/')

        else:
            return HttpResponse("Invalid login details")

@csrf_exempt
def student_profile(request):

    dic={}

    if request.method == "GET":
        user_info = Student.objects.raw("select * from student where username=%s",[request.user])

        for u in user_info:
            
            dic['name'] = u.name
            dic['dob'] = u.dob
            dic['gender'] = u.gender
            dic['address'] = u.address
            dic['mobno'] = u.mobno
            dic['email'] = u.email
            dic['course'] = u.course
            dic['branch'] = u.branch
            dic['cgpa'] = u.cgpa
            dic['arrears'] = u.arrears
            dic['sslc'] = u.sslc
            dic['plustwo'] = u.plustwo
            dic['username'] = u.username 


    
        return render(request, 'profile_stud.html', dic)
    else:
        cgpa = request.POST.get('cgpa')
        course = request.POST.get('course')
        branch = request.POST.get('branch')
        arrears = request.POST.get('arrears')

        l=[]
        response={}
        obj = job.objects.raw("select * from job where mincgpa<=%s and maxarrears>=%s and branch=%s and course=%s", [cgpa , arrears , branch , course])
        for j in obj:
            dic={}
            dic['salary'] = j.salary
            dic['jobtype'] = j.jobtype

            print(j.salary)
            print(j.jobtype)

            l.append(dic)
        response['data'] = l

        print(response)
        return JsonResponse(response)

def company_profile(request):

    dic = {}
    user_info = User.objects.raw("select * from pms.auth_user where username=%s",[request.user])
    for u in user_info:
        id  = u.id
    
    user_info = Company.objects.raw("select * from company where compid=%s",[id])
    for u in user_info:
        
        dic['name'] = u.compname
        dic['address'] = u.address
        dic['contactno'] = u.contactno
        dic['contactemail'] = u.contactemail

    
    l=[]

    job_info= job.objects.raw("select * from job where compid_id=%s",[id])
    for u in job_info:
        dict2={}
        dict2['jobtype'] = u.jobtype
        dict2['course'] = u.course
        dict2['branch'] = u.branch
        dict2['salary'] = u.salary
        dict2['mincgpa'] = u.mincgpa
        dict2['maxarrears'] = u.maxarrears
        l.append(dict2)
    dic['data'] = l

    

    return render(request, 'profile_comp.html', dic )

def register(request):

    if request.method == 'POST':

        

        name = request.POST.get('name')
        birth_day = request.POST.get('birthday')
        gender = request.POST.get('gender')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        address = request.POST.get('address')
        regno = request.POST.get('regno')
        course = request.POST.get('course')
        branch = request.POST.get('branch')
        cgpa = request.POST.get('cgpa')
        arrears = request.POST.get('arrears')
        sslc = request.POST.get('sslc')
        plus_two = request.POST.get('plustwo')
        username=request.user
        var=Student.objects.raw("select * from  student where id=(select max(id) from student)")
        for i in var:
            id=i.id
        print(id)

        with connection.cursor() as cursor:
            cursor.execute("insert into student values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", [id+1,name,birth_day,gender,address,mobile,email,course,branch,cgpa,arrears,sslc,plus_two,username])





        return redirect('/student_profile')


    print (request.user)
    return render(request, 'register.html')

def company(request):
    return render(request, 'company.html', {})

def jobinfo(request):

    if request.method == 'POST':

        name = request.POST.get('name')
        jobtype = request.POST.get('jobtype')
        course = request.POST.get('course')
        branch = request.POST.get('branch')
        salary = request.POST.get('salary')
        mincgpa = request.POST.get('mincgpa')
        maxarrears = request.POST.get('maxarrears')

        info = Company.objects.raw(" select * from company where compname=%s",[name])
        for j in info:
            compid = j.compid

        info = job.objects.raw("select * from job where jobid=(select max(jobid) from job)")
        jobid=0
        for  j in info:
            if (j.jobid is None):
                jobid=0
            else:
                jobid = j.jobid
        with connection.cursor() as cursor:
            cursor.execute("insert into job values(%s,%s,%s,%s,%s,%s,%s,%s)",[jobid+1 , jobtype , course , branch , salary ,mincgpa , maxarrears , compid])
        
        return  redirect('/company_profile')

    return render(request, 'jobinfo.html', {})

def logoutfn(request):
    logout(request)

    return redirect('/')