from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.mixins import AuthRequiredMixin, DeleteProtectionMixin
from .models import Status
from .forms import StatusForm


class StatusesListView(AuthRequiredMixin, ListView):
    template_name = 'statuses/statuses.html'
    model = Status
    context_object_name = 'statuses'


class StatusBaseView(AuthRequiredMixin, SuccessMessageMixin):
    template_name = 'form.html'
    model = Status
    form_class = StatusForm
    success_url = reverse_lazy('statuses')


class StatusCreateView(StatusBaseView, CreateView):
    success_message = _('Status successfully created')


class StatusUpdateView(StatusBaseView, UpdateView):
    success_message = _('Status successfully changed')


class StatusDeleteView(
    AuthRequiredMixin, DeleteProtectionMixin, SuccessMessageMixin, DeleteView
):
    template_name = 'statuses/delete.html'
    model = Status
    success_url = reverse_lazy('statuses')
    success_message = _('Status successfully deleted')
    protected_message = _(
        'It is not possible to delete a status because it is in use')
    protected_url = reverse_lazy('statuses')
