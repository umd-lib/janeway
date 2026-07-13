import os

from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple

from plugins.customstyling import plugin_settings, widgets, models


class StylingForm(forms.Form):
    css = forms.CharField(
        widget=widgets.CodeEditor,
    )

    def __init__(self, *args, **kwargs):
        self.journal = kwargs.pop('journal', None)
        self.repository = kwargs.pop('repository', None)
        super(StylingForm, self).__init__(*args, **kwargs)
        if self.journal:
            open_path = os.path.join(
                plugin_settings.BASE_CSS_PATH,
                str(self.journal.pk),
                'custom.css',
            )
        elif self.repository:
            open_path = os.path.join(
                plugin_settings.BASE_CSS_PATH,
                'repositories',
                str(self.repository.pk),
                'custom.css',
            )
        else:
            open_path = os.path.join(
                plugin_settings.BASE_CSS_PATH,
                'press',
                'custom.css'
            )

        if os.path.isfile(open_path):
            with open(open_path) as css_file:
                css = css_file.read()
                self.fields['css'].initial = css
        else:
            self.fields['css'].initial = '/* Insert CSS Below */'

    def save(self):
        css = self.cleaned_data['css']

        if self.journal:
            path = os.path.join(
                plugin_settings.BASE_CSS_PATH,
                str(self.journal.pk),
            )
        elif self.repository:
            path = os.path.join(
                plugin_settings.BASE_CSS_PATH,
                'repositories',
                str(self.repository.pk),
            )
        else:
            path = os.path.join(
                plugin_settings.BASE_CSS_PATH,
                'press',
            )

        file = os.path.join(path, 'custom.css')
        if not os.path.exists(path):
            os.makedirs(path)

        with open(file, 'w') as css_file:
            css_file.write(css)
            css_file.close()


class CrossJournalStylingForm(forms.ModelForm):
    css = forms.CharField(
        widget=widgets.CodeEditor,
    )

    class Meta:
        model = models.CrossJournalStylesheet
        fields = ('journals',)
        widgets = {
            'journals': FilteredSelectMultiple(
                "Journals",
                False,
                attrs={'rows': '2'},
            )
        }

    field_order = ['css', 'journals']

    def __init__(self, *args, **kwargs):
        super(CrossJournalStylingForm, self).__init__(*args, **kwargs)
        open_path = os.path.join(
            plugin_settings.BASE_CSS_PATH,
            'press',
            self.instance.stylesheet_name
        )
        if self.instance.pk and os.path.isfile(open_path):
            with open(open_path) as css_file:
                css = css_file.read()
                self.fields['css'].initial = css
        else:
            self.fields['css'].initial = '/* Insert CSS Below */'

    def save(self, commit=True):
        stylesheet = super(CrossJournalStylingForm, self).save(commit=False)
        css = self.cleaned_data['css']

        path = os.path.join(
            plugin_settings.BASE_CSS_PATH,
            'press',
        )
        file = os.path.join(path, stylesheet.stylesheet_name)
        if not os.path.exists(path):
            os.makedirs(path)

        with open(file, 'w') as css_file:
            css_file.write(css)
            css_file.close()

        if commit:
            stylesheet.save()

        return stylesheet