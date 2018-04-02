from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, StreamingHttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.forms import AuthenticationForm
from urllib.parse import quote

from .models import UploadFile, ContentType
from .forms import UploadFileForm


def index(request):
    return render(request, 'YunPan/index.html')


def public(request):
    files = UploadFile.objects.filter(file_type='public')[::-1]
    return render(request, 'YunPan/public.html', {'files': files})


@login_required
def private(request):
    files = UploadFile.objects.filter(user=request.user)[::-1]
    return render(request, 'YunPan/private.html', {'files': files})


@login_required
def change_file_type(request, pk):
    file = UploadFile.objects.get(user=request.user, id=pk)
    if file.file_type == 'public':
        file.file_type = 'private'
    elif file.file_type == 'private':
        file.file_type = 'public'
    file.save()
    return render(request, 'YunPan/message.html', {'message': '移动成功'})


@login_required
def delete_file(request, pk):
    file = UploadFile.objects.get(user=request.user, id=pk)
    file.upload.delete()
    file.delete()
    return render(request, 'YunPan/message.html', {'message': '删除成功'})


@login_required
def download_private_file(request, pk):
    file = UploadFile.objects.get(user=request.user, id=pk)

    def file_iterator(chunk_size=512):
        while True:
            c = file.upload.read(chunk_size)
            if c:
                yield c
            else:
                break

    response = StreamingHttpResponse(file_iterator())
    response['Content-Type'] = ContentType.get(file.upload.name.split('.')[-1], 'application/octet-stream')
    response['Content-Disposition'] = 'attachment;filename="%s"' % quote(file.upload.name.split('/')[-1])
    return response


def download_file(request, pk):
    file = UploadFile.objects.get(id=pk)
    if file.file_type != 'public':
        return render(request, 'YunPan/message.html', {'message': '拒绝访问'})

    def file_iterator(chunk_size=512):
        while True:
            c = file.upload.read(chunk_size)
            if c:
                yield c
            else:
                break

    response = StreamingHttpResponse(file_iterator())
    response['Content-Type'] = ContentType.get(file.upload.name.split('.')[-1], 'application/octet-stream')
    response['Content-Disposition'] = 'attachment;filename="%s"' % quote(file.upload.name.split('/')[-1])
    return response


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
