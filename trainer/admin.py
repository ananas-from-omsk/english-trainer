"""Admin configuration for trainer app"""

from django.contrib import admin
from .models import Word

admin.site.register(Word)
