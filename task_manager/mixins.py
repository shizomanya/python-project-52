from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.db.models import ProtectedError
from django.views import View
from task_manager.users.models import User


class AuthRequiredMixin(LoginRequiredMixin):
    auth_message = _('You are not logged in! Please log in.')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, self.auth_message)
            return redirect(reverse_lazy('login'))
        return super().dispatch(request, *args, **kwargs)


class UserPermissionMixin(UserPassesTestMixin):
    permission_message = _('You do not have permission to modify this user.')
    permission_url = '/'

    def test_func(self):
        user_id = self.kwargs['pk']
        user = User.objects.get(id=user_id)
        return user == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, self.permission_message)
        return redirect(self.permission_url)


class DeleteProtectionMixin(View):
    protected_message = _('This user cannot be deleted as it is being used.')
    protected_url = '/'

    def post(self, request, *args, **kwargs):
        try:
            return super().post(request, *args, **kwargs)
        except ProtectedError:
            messages.error(request, self.protected_message)
            return redirect(self.protected_url)


class AuthorDeletionMixin(UserPermissionMixin):
    author_message = _('You do not have permission to delete this item.')
    author_url = '/'

    def handle_no_permission(self):
        messages.error(self.request, self.author_message)
        return redirect(self.author_url)
