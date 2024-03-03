from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from tracker.models import create_new_task


@csrf_exempt
def create_task(request, *args, **kwargs):
    data = request.POST
    task_data = json.loads(request.body.decode('utf-8'))
    create_new_task(description=task_data.get('description'))
    return HttpResponse('ok', status=200)
