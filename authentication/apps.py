#תצורת האפליקציה בפרוייקט
from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField' #סוג השדה שישמש לשדות במודלים
    name = 'authentication'
