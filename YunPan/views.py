from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm

from .models import UploadFile
from .forms import UploadFileForm


def index(request):
    return render(request, 'YunPan/index.html')


@login_required
def upload_file(request):
    if request.method != 'POST':
        form = UploadFileForm()
    else:
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file = UploadFile(user=request.user, upload=form.cleaned_data['upload'],
                              file_type=form.cleaned_data['file_type'])
            file.save()
            return render(request, 'YunPan/message.html', {'message': '上传成功！'})
    return render(request, 'YunPan/upload_file.html', {'form': form})


def login(request):
    redirect_to = request.GET.get('next', '/')
    if request.method != 'POST':
        form = AuthenticationForm()
    else:
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            auth_login(request, form.user_cache)
            return HttpResponseRedirect(redirect_to)
    return render(request, 'YunPan/login.html', {'form': form})


def register(request):
    return render(request, 'YunPan/message.html', {'message': '请先登录后注册'})


@login_required()
def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('YunPan:index'))
