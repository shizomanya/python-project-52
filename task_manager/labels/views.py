from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.mixins import AuthRequiredMixin, DeleteProtectionMixin
from .models import Label
from .forms import LabelForm


class LabelsListView(AuthRequiredMixin, ListView):
    template_name = 'labels/labels.html'
    model = Label
    context_object_name = 'labels'


class LabelBaseView(AuthRequiredMixin, SuccessMessageMixin):
    template_name = 'form.html'
    model = Label
    form_class = LabelForm
    success_url = reverse_lazy('labels')


class LabelCreateView(LabelBaseView, CreateView):
    success_message = _('Label successfully created')


class LabelUpdateView(LabelBaseView, UpdateView):
    success_message = _('Label successfully changed')


class LabelDeleteView(
    AuthRequiredMixin, DeleteProtectionMixin, SuccessMessageMixin, DeleteView
):
    template_name = 'labels/delete.html'
    model = Label
    success_url = reverse_lazy('labels')
    success_message = _('Label successfully deleted')
    protected_message = _('It is not possible to delete a label '
                          'because it is in use')
    protected_url = reverse_lazy('labels')
