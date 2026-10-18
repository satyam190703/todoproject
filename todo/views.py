from django.shortcuts import render,redirect,get_object_or_404
from django.urls import reverse
from django.http import HttpResponse
from . import models

# Create your views here.
def create_task(request):
    print(request.POST)
    if request.method=='POST':
        title=request.POST.get('title','').strip()
        description=request.POST.get('description','').strip()
        if not title:
            return HttpResponse('Title Cannot be empty')
        models.Task.objects.create(title=title,description=description)
        return redirect(reverse('todo:task_list'))
    return render(request,'todo/task_form.html')

def task_list(request):
    tasks=models.Task.objects.all()
    return render(request,'todo/task_list.html',{'tasks':tasks})

def update_task(request,pk):
    task=get_object_or_404(models.Task,pk=pk)
    if request.method=='POST':
        task.title=request.POST.get('title','').strip()
        if not task.title:
            return HttpResponse('Title cannot be empty')
        task.description=request.POST.get('description','').strip()
        task.completed=request.POST.get('completed')=='on'
        task.save()
        return redirect(reverse('todo:task_list'))
    return render(request,'todo/task_form.html',{'task':task})

def delete_task(request,pk):
    task=get_object_or_404(models.Task,pk=pk)
    if request.method=='POST':
        task.delete()
        return redirect(reverse('todo:task_list'))
    return render(request,'todo/delete_confirmation.html',{'task':task})

def toggle_task(request,pk):
    task=get_object_or_404(models.Task,pk=pk)
    task.completed=not task.completed
    task.save()
    return redirect(reverse('todo:task_list'))