from django.shortcuts import render
#from django.template.loader import get_template
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    JsonResponse,
)
import logging
import datetime
import re
import collector.filehandler as filehandler
from .models import File

# Create your views here.

def time(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)

@login_required
def old(request):
    num_files = File.objects.count()

    return HttpResponse(render(
        request,
        'collector.html', dict(
        num_files=num_files,
    )))

@login_required
def index(request):

    return HttpResponse(render(
        request,
        'vue.html'
    ))

@csrf_exempt
@login_required
def upload(request):
    ret = []
    if request.method == 'POST':
        for key in request.FILES.keys():
            for file in request.FILES.getlist(key):
                ret.append(filehandler.save_request_file(file, request.user))

        return HttpResponseRedirect('..')
#        return HttpResponse('files: {}'.format(ret))
    else:
        return HttpResponseRedirect('..')

@login_required
def delete_files(request):
    if request.method != 'POST':
        return HttpResponse(status=405)
    ret = []
    for key, value in request.POST.items():
        if re.match('[0-9]+$', key):
            success = filehandler.delete_file(int(key))
            ret.append(dict(id=key, success=success))

#    return HttpResponse('deleted: {}'.format(ret))
    return HttpResponseRedirect('..')


@login_required
def process_files(request):
    if request.method != 'POST':
        return HttpResponse(status=405)
    ret = []
    for key, value in request.POST.items():
        if re.match('[0-9]+$', key):
            task_id = filehandler.process_file(int(key))
            ret.append(dict(id=key, task_id=task_id))

    return JsonResponse({
        'success': True,
        'results': ret
    })




views = [index, time, upload, delete_files, process_files, old]
