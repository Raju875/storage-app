from importlib import import_module
from pathlib import Path

from django.conf import settings


try:
    modules_dir = f"{settings.BASE_DIR}/modules/"
    admins = list(Path(modules_dir).rglob('admin.py'))

    for admin in admins:
        module_name, _ = admin.as_posix().split('/')[-2:]
        if not module_name == "modules":
            module = import_module(f"modules.{module_name}.admin")
            from module import *  # noqa
except (ImportError, IndexError):
    pass
