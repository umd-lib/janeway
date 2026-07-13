from django.shortcuts import render, get_object_or_404, reverse, redirect
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required

from plugins.customstyling import forms, models, security, plugin_settings
from journal import models as jm
from repository import models as rm
from utils import setting_handler
from core.forms import GeneratedSettingForm


@security.user_is_staff_or_journal_editor
def manager(request):
    cjs_list = models.CrossJournalStylesheet.objects.all()
    template = 'customstyling/manager.html'

    context = {
        'journals': jm.Journal.objects.all(),
        'repositories': rm.Repository.objects.all(),
        'cjs_list': cjs_list,
    }

    return render(request, template, context)


@staff_member_required
def settings(request):
    form_settings = [
        {
            'name': 'enable_editor_access',
            'object': setting_handler.get_setting(
                plugin_settings.CustomstylingPlugin.plugin_group_name,
                'enable_editor_access',
                request.journal,
            ),
        },
    ]
    form = GeneratedSettingForm(
        settings=form_settings,
    )
    if request.POST:
        form = GeneratedSettingForm(
            request.POST,
            settings=form_settings,
        )
        if form.is_valid():
            form.save(
                journal=request.journal,
                group=plugin_settings.CustomstylingPlugin.plugin_group_name,
            )
            return redirect(
                reverse(
                    'customstyling_settings'
                )
            )

    template = 'customstyling/settings.html'
    context = {
        'form': form,
    }
    return render(
        request,
        template,
        context,
    )


@security.staff_or_editor_access_enabled
def manage_css(request, journal_id=None, repository_id=None):
    journal = repository = None
    if journal_id:
        journal = get_object_or_404(
            jm.Journal,
            pk=journal_id,
        )
    elif repository_id:
        repository = get_object_or_404(
            rm.Repository,
            pk=repository_id
        )
    form = forms.StylingForm(
        journal=journal,
        repository=repository,
    )
    if request.POST:
        form = forms.StylingForm(
            request.POST,
            journal=journal,
            repository=repository,
        )
        if form.is_valid():
            form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                'Saved.',
            )
            if journal:
                reversed_url = reverse(
                    'customstyling_manage_css_journal',
                    kwargs={
                        'journal_id': journal.pk,
                    }
                )
            elif repository:
                reversed_url = reverse(
                    'customstyling_manage_css_repository',
                    kwargs={
                        'repository_id': repository.pk,
                    }
                )
            return redirect(
                reversed_url
            )
    template = 'customstyling/manage_css.html'
    context = {
        'journal': journal,
        'form': form,
    }
    return render(request, template, context)


@staff_member_required
def manage_press_css(request):
    form = forms.StylingForm()
    if request.POST:
        form = forms.StylingForm(
            request.POST,
        )
        if form.is_valid():
            form.save()
            messages.add_message(
                request,
                messages.SUCCESS,
                'Saved.',
            )
            return redirect(
                reverse(
                    'customstyling_manage_press_css',
                )
            )

    template = 'customstyling/manage_css.html'
    context = {
        'form': form,
    }
    return render(request, template, context)


@staff_member_required
def manage_cross_journal_stylesheets(request, stylesheet_id=None):
    stylesheet = None
    if stylesheet_id:
        stylesheet = get_object_or_404(
            models.CrossJournalStylesheet,
            pk=stylesheet_id,
        )
    form = forms.CrossJournalStylingForm(
        instance=stylesheet,
    )
    if request.POST:
        form = forms.CrossJournalStylingForm(
            request.POST,
            instance=stylesheet,
        )
        if form.is_valid():
            stylesheet = form.save()
            form.save_m2m()

            return redirect(
                reverse(
                    'customstyling_edit_lcjsc',
                    kwargs={
                        'stylesheet_id': stylesheet.pk,
                    }
                )
            )

    template = 'customstyling/manage_cross_journal_stylesheet.html'
    context = {
        'stylesheet': stylesheet,
        'form': form,
    }
    return render(
        request,
        template,
        context,
    )
