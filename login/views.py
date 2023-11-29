from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import  authenticate,login,logout

def logins(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user:
            login(request,user)
            return redirect('/')
        else:
            msg='帳號密碼輸入錯誤'
            return render(request,'login.html',locals())
    return render(request,'login.html')

def register(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        password2=request.POST.get('password2')
        email=request.POST.get('email')
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        if password != password2:
            msg='兩次輸入密碼不同'
            return render(request,'register.html',locals())
        elif username == '':
            msg='用戶名不得為空'
            return render(request,'register.html',locals())
        elif User.objects.filter(username=username).exists():
            msg='用戶名已經存在'
            return render(request,'register.html',locals())
        elif email=='':
            msg='mail不可為空'
            return render(request,'register.html',locals())
        elif first_name=='':
            msg='名稱不可為空'
            return render(request,'register.html',locals())
        u = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        u.save()
        return redirect('/login/')
    return render(request,'register.html')

def logouts(request):
    logout(request)
    return redirect('/')