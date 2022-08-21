from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class ModulesConfig(AppConfig):
    name = 'modules'
    verbose_name = _('Core Modules')
