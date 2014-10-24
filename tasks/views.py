from django.shortcuts import get_object_or_404, render_to_response, render
from django.template import RequestContext
from django.http import HttpResponse
from tasks.models import Task
from tasks.forms import TaskForm
import json as simplejson
from django.utils import dateformat, timezone
from datetime import datetime
import pytz

def tasks(request):
	context = {}
	utc=pytz.UTC
	nowtime = utc.localize(datetime.now())

	if request.method == 'POST':
		form = TaskForm(request.POST)
		if form.is_valid():
			task = form.save()
			record = {'id': task.id, 'title': task.title, 
				'edate': dateformat.format(task.expiration_date, 'F j, Y, P')}
			data = {'status': 'ok', 'messageType': 'addTask', 'record': record}
		else:
			data = {'status': 'error', 'messageType': 'showErrors', 'record': form.errors}
		return 	HttpResponse(simplejson.dumps(data), content_type='application/json')	
	else:		
		form = TaskForm()

	context['form'] = form
	tasks = Task.objects.filter(is_deleted = False)

	for task in tasks:
		if task.is_expired == False and task.expiration_date < nowtime:
			task.is_expired = True
			task.save()
	context['tasks'] = tasks

	return render_to_response('tasks/tasks.html', context, 
		context_instance=RequestContext(request))


def delete_task(request):
	data = {}
	if request.method == 'POST':
		tid = request.POST.get('tid')
		if tid:
			task = Task.objects.get(id = int(tid))
			if task:
				task.is_deleted = True
				task.save()
				data['status'] = 'ok'	
			else:	
				data['status'] = 'task not found'	
		else:
			data['status'] = 'fid not found'
	else:				
		data['status'] = 'No POST'

	return HttpResponse(simplejson.dumps(data), content_type='application/json')

def complete_task(request):
	data = {}
	if request.method == 'POST':
		tid = request.POST.get('tid')
		checked = request.POST.get('checked')
		if tid:
			task = Task.objects.get(id = int(tid))
			if task:
				if checked == 'true':
					task.is_completed = True
				else:
					task.is_completed = False
				task.save()
				data['status'] = 'ok'	
			else:	
				data['status'] = 'task not found'	
		else:
			data['status'] = 'fid not found'
	else:				
		data['status'] = 'No POST'
		
	return HttpResponse(simplejson.dumps(data), content_type='application/json')					

