from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import encryption 
import os
from django.contrib import messages
from django.contrib.auth.models import User,auth
from .models import Files

# Create your views here.
def home(request):
    if request.user.id!=None:
        files = Files.objects.all().filter(user=request.user).order_by('date')
        return render(request,'home.html',{'files':files})
    return render(request,'home.html')


def enyc(request):
    # print(request.POST['file'])
    current_path=(os.getcwd())
    myfile = request.FILES['file1']
    fs = FileSystemStorage() #defaults to   MEDIA_ROOT 
   
    filename = fs.save(myfile.name, myfile)
    file_url = fs.url(filename)
    f = Files.objects.create(user=request.user,title=filename)
    key = b'[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e'
    enc = encryption.Encryptor(key) 
    os.chdir(current_path+"\media")
    enc.encrypt_file(filename)  
    os.chdir(current_path)
    messages.info(request,"Encryption Successful!!")
    return redirect('/')


def deyc(request):
    # print(request.POST['file'])
    try:
        file = str(request.POST['file'])
        current_path=(os.getcwd())
        key = b'[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e'
        enc = encryption.Encryptor(key) 
        os.chdir(current_path+"\media")        
        file_name = file +".enc"
        enc.decrypt_file(file_name) 
        with open(file, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file)
        os.remove(file)
        os.chdir(current_path)
        f = Files.objects.get(title=file)
        f.delete()
        return response
    except:
        messages.info(request,"Please select a file to decrypt")
        return redirect('/') 
    # os.chdir(current_path)
    # return HttpResponse('Decryption Done')


def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,"Invalid Credientials")
            return redirect('login')
    else:
        return render(request,'login.html')

def logout(request):
    auth.logout(request)
    return redirect('/')


def signup(request):
    if request.method=='POST':
        username=request.POST['username']
        password1=request.POST['password1']
        password2=request.POST['password2']
        email=request.POST['email']
        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,"Username Taken")
                return redirect('signup')
            else:
                user=User.objects.create_user(username=username,email=email,password=password1)
                user.save()
                return redirect('login')
        else:
            messages.info(request,"Password Not Matching!") 
            return redirect('register')   
        return redirect('/')
    else:
        return render(request,'signup.html')