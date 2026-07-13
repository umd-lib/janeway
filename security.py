from functools import wraps

from django.shortcuts import redirect, reverse

from plugins.customstyling import plugin_settings
from core import models
from utils import setting_handler
from security.decorators import base_check_required, deny_access


def user_is_staff_or_journal_editor(func):
    """
    Determines if a user is staff, or if Editor Access is enabled and there is a request.journal: directs them
    to the edit page.
    """

    @base_check_required
    def wrapper(request, *args, **kwargs):
        if request.user.is_staff or request.user.is_admin or request.user.is_superuser:
            return func(request, *args, **kwargs)

        if request.journal:
            editor_acccess_enabled = setting_handler.get_setting(
                setting_group_name=plugin_settings.CustomstylingPlugin.plugin_group_name,
                setting_name='enable_editor_access',
                journal=request.journal,
                default=True,
            ).processed_value

            if editor_acccess_enabled and request.user.is_editor(request):
                return redirect(
                    reverse(
                        'customstyling_manage_css_journal',
                        kwargs={
                            'journal_id': request.journal.pk,
                        }
                    )
                )

        return deny_access(request)

    return wrapper


def staff_or_editor_access_enabled(func):

    def wrapper(request, *args, **kwargs):
        if request.user.is_staff or request.user.is_admin or request.user.is_superuser:
            return func(request, *args, **kwargs)

        if request.journal:
            editor_acccess_enabled = setting_handler.get_setting(
                setting_group_name=plugin_settings.CustomstylingPlugin.plugin_group_name,
                setting_name='enable_editor_access',
                journal=request.journal,
                default=True,
            ).processed_value

            if editor_acccess_enabled and request.user.is_editor(request):
                return func(request, *args, **kwargs)

            return deny_access(request)

    return wrapper