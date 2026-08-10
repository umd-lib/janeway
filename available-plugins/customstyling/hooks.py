import os

from plugins.customstyling import plugin_settings, models
from utils.function_cache import cache


@cache(900)
def inject_css(context):
    request = context['request']
    html = ''
    if request.journal:
        cross_journal_stylesheets = models.CrossJournalStylesheet.objects.filter(
            journals=request.journal,
        )
        for stylesheet in cross_journal_stylesheets:
            html += '<link href="{}" rel="stylesheet">\n'.format(
                os.path.join(plugin_settings.CSS_MEDIA_PATH, 'press', stylesheet.stylesheet_name)
            )
        html += '<link href="{}" rel="stylesheet">\n'.format(
            os.path.join(plugin_settings.CSS_MEDIA_PATH, str(request.journal.pk), 'custom.css')
        )
    elif request.repository:
        html += '<link href="{}" rel="stylesheet">\n'.format(
            os.path.join(
                plugin_settings.CSS_MEDIA_PATH,
                'repositories',
                str(request.repository.pk),
                'custom.css',
            )
        )
    else:
        html += '<link href="{}" rel="stylesheet">\n'.format(
            os.path.join(plugin_settings.CSS_MEDIA_PATH, 'press', 'custom.css')
        )

    return html
