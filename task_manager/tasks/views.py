from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, DetailView
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from django_filters.views import FilterView
from task_manager.mixins import AuthRequiredMixin, AuthorDeletionMixin
from .models import Task
from .forms import TaskForm, TaskFilter


class TasksListView(AuthRequiredMixin, FilterView):
    template_name = 'tasks/tasks.html'
    model = Task
    filterset_class = TaskFilter
    context_object_name = 'tasks'


class TaskDetailView(AuthRequiredMixin, DetailView):
    template_name = 'tasks/task_show.html'
    model = Task
    context_object_name = 'task'


class TaskCreateView(AuthRequiredMixin, SuccessMessageMixin, CreateView):
    template_name = 'form.html'
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks')
    success_message = _('Task successfully created')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class TaskUpdateView(AuthRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'form.html'
    model = Task
    form_class = TaskForm
    success_url = reverse_lazy('tasks')
    success_message = _('Task successfully changed')


class TaskDeleteView(
    AuthRequiredMixin, AuthorDeletionMixin, SuccessMessageMixin, DeleteView
):
    template_name = 'tasks/delete.html'
    model = Task
    success_url = reverse_lazy('tasks')
    success_message = _('Task successfully deleted')
    author_message = _('The task can be deleted only by its author')
    author_url = reverse_lazy('tasks')
