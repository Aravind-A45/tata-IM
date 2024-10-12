from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User, Group, auth
from .models import *
from  django.contrib import messages
from .tasks import *

# Create your views here.
def admins(request):
    is_admin = request.user.groups.filter(name='Admin').exists()
    error_message = None
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        file_obj = File.objects.create(file=uploaded_file)
        messages.info(request, "File uploaded")

        task_result = process_excel_file.delay(file_obj.id, request.user.id)
        if isinstance(task_result.result, str):
            error_message = task_result.result
    return render(request, "admin/admins.html", {"is_admin":is_admin, 'error_message': error_message})

def home(request):
  is_admin = request.user.groups.filter(name='admin').exists()
  return render(request, "home.html", {"is_admin":is_admin})

def login(request):
    if request.user.is_authenticated :
      return redirect('home')

    if request.method=='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        try:
            user=auth.authenticate(username=username,password=password, email=email) 
            if user != None:
                auth.login(request,user)
                return redirect('home')
            else:
                messages.info(request, "Invalid credentials")
                return redirect('signup')
        except:
            return redirect('login')
 
    return render(request,'credentials/login.html')

def signup(request):
    details = User.objects.all()

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        con_password = request.POST.get('con_password')
        email = request.POST.get('email')
        
        if password == con_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, f"Username already exists")
                return redirect('signup')

            if User.objects.filter(email=email).exists():
                messages.info(request, f"Email already exists")
                return redirect('signup')

            user = User.objects.create_user(username=username, password=password, email=email)
            user = authenticate(username=username, password=password, email=email)
            student_group = Group.objects.get(name='user')
            user.groups.add(student_group)

            info_id = request.session.get('info_id')
            if info_id:
                info = Info.objects.get(id=info_id)
                info.user = user
                info.save()
                del request.session['info_id']
            messages.success(request, "Account created successfully.")

            if user is not None:
                return redirect('login')
            else:
                messages.error(request, "Invalid username or password.")   
        else:
          messages.error(request, "Password and Confirm Password are not matching")
    return render(request, 'credentials/signup.html')

def logout(request):
  auth.logout(request)
  return redirect('login')  