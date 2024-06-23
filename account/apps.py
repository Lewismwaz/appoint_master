from importlib import import_module
from django.apps import AppConfig

# This is the AppConfig class for the account app. It is used to import the signals module when the app is ready.
class YourAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'account'

    # This method is called when the app is ready. It imports the signals module.
    def ready(self):
        import_module('.signals', package='account') 