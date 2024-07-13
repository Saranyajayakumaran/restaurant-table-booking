"""standard imports"""
from django.apps import AppConfig


class BookingAppConfig(AppConfig):
    """
    AppConfig subclass for configuring the 'booking_app' application.

    This class defines configuration settings specific to the 'booking_app'
    Django application. It sets the default database auto-generated field
    to 'BigAutoField' for models within this app.

    Attributes:
        default_auto_field (str): Specifies the default auto-generated field
            type for models in this app as 'django.db.models.BigAutoField'.
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'booking_app'
