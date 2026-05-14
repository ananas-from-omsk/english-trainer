"""App configuration for trainer"""

from django.apps import AppConfig

class TrainerConfig(AppConfig):
    """Configuration for trainer app"""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'trainer'