import os

from django.conf import settings

from utils import plugins, setting_handler

PLUGIN_NAME = 'Custom Styling Plugin'
DISPLAY_NAME = 'Custom Styling'
DESCRIPTION = 'Allows staff to add custom css to journals.'
AUTHOR = 'Andy Byers'
VERSION = '1.0'
SHORT_NAME = 'customstyling'
MANAGER_URL = 'customstyling_manager'
JANEWAY_VERSION = "1.5.0"
BASE_CSS_PATH = os.path.join(
    settings.MEDIA_ROOT,
    'customstyling',
)
CSS_MEDIA_PATH = os.path.join(
    settings.MEDIA_URL,
    'customstyling',
)


class CustomstylingPlugin(plugins.Plugin):
    plugin_name = PLUGIN_NAME
    display_name = DISPLAY_NAME
    description = DESCRIPTION
    author = AUTHOR
    short_name = SHORT_NAME
    manager_url = MANAGER_URL

    version = VERSION
    janeway_version = JANEWAY_VERSION
    press_wide = True
    plugin_group_name = 'plugin:{plugin_name}'.format(plugin_name=SHORT_NAME)
    

def install():
    CustomstylingPlugin.install()
    setting_handler.create_setting(
        setting_group_name=CustomstylingPlugin.plugin_group_name,
        setting_name='enable_editor_access',
        pretty_name='Enable Editor Access',
        type='boolean',
        description='If enabled, editors can access the css plugin.',
        is_translatable=False,
        default_value=' ',
    )


def hook_registry():
    return {
        'base_head_css':
            {
                'module': 'plugins.customstyling.hooks',
                'function': 'inject_css',
            },
    }


def register_for_events():
    pass
