from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from tasks.mixins import UserIsOwnerMixin
from tasks import models
from tasks.forms import TaskForm, TaskFilterForm, CommentForm
from django.contrib.auth import login
from django.contrib.auth.views import LoginView, LogoutView 
# Create your views here.
class TaskListView(ListView):
    model = models.Task
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = super().get_queryset()
        status = self.request.GET.get('status', '')
        if status:
            queryset= queryset.filter(status = status)
        return queryset    

    def get_context_data (self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["form"] = TaskFilterForm(self.request.GET)
        return context



class TaskDetailView(DetailView):
    model = models.Task
    context_object_name = 'task'    
    CommentForm
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comment_form'] = CommentForm()
        return context
    
    def post(self, request ,*args, **kwargs):
        comment_form= CommentForm(request.POST, request.FILES)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.task = self.get_object()
            comment.save()
            return redirect('tasks:task-detail', pk = comment.task.pk)

class TaskCreatelView(CreateView):
    model = models.Task
    form_class = TaskForm    
    success_url = reverse_lazy('tasks:task-list')

class TaskUpdateView(LoginRequiredMixin, UserIsOwnerMixin ,UpdateView):
    model = models.Task
    form_class = TaskForm   
    success_url = reverse_lazy('tasks:task-list')

class TaskDeleteView(LoginRequiredMixin, DeleteView):
    model = models.Task
    success_url = reverse_lazy('tasks:task-list')

class CustomLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'tasks/login.html'