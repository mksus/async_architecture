from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
from tracker.models import create_new_task, reassign_tasks as reassign_task_logic, complete_task as complete_task_logic


# todo нужно будет переделать на generics и заюзать PermissionClass из django-oauth-toolkit. Не разобрался до конца.

@csrf_exempt
def create_task(request, *args, **kwargs):
    data = request.POST
    task_data = json.loads(request.body.decode('utf-8'))
    create_new_task(description=task_data.get('description'))
    return HttpResponse('ok', status=200)


# todo ограничить права
@csrf_exempt
def reassign_tasks(request, *args, **kwargs):
    data = request.POST
    reassign_task_logic()
    return HttpResponse('ok', status=200)


@csrf_exempt
def complete_task(request, *args, **kwargs):
    data = request.POST
    task_data = json.loads(request.body.decode('utf-8'))
    task_id = task_data.get('task_id')
    print(task_id, request.user.id)
    complete_task_logic(task_id=task_id, user_id=request.user.id)
    return HttpResponse('ok', status=200)
