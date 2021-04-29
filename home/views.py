from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import encryption 
import os

# Create your views here.
def home(request):
    return render(request,'home.html')


def enyc(request):
    # print(request.POST['file'])
    current_path=(os.getcwd())
    myfile = request.FILES['file1']
    fs = FileSystemStorage() #defaults to   MEDIA_ROOT 
   
    filename = fs.save(myfile.name, myfile)
    file_url = fs.url(filename)
    key = b'[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e'
    enc = encryption.Encryptor(key) 
    os.chdir(current_path+"\media")
    enc.encrypt_file(filename)  
    return HttpResponse('Done')


def deyc(request):
    # print(request.POST['file'])
    current_path=(os.getcwd())
    key = b'[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e'
    enc = encryption.Encryptor(key) 
    os.chdir(current_path+"\media")
    l=os.listdir()
    print(l)
    enc.decrypt_file(l[0])  
    return HttpResponse('Done')