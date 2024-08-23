from django.apps import AppConfig
from django.conf import settings
import os


class AccountsConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "accounts"

    def ready(self):
        # Ensure MEDIA_ROOT directory exists
        media_root = settings.MEDIA_ROOT
        try:
            if not os.path.exists(media_root):
                os.makedirs(media_root)
                print(f"Created MEDIA_ROOT directory at {media_root}")
        except PermissionError:
            print(f"Permission denied: Cannot create MEDIA_ROOT directory at {media_root}")
