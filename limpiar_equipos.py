#!/usr/bin/env python
"""
Script para limpiar equipos existentes antes de migrar a ForeignKey
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cerveceros_tecate.settings')
django.setup()

from equipo.models import Equipo

# Eliminar todos los equipos existentes
count = Equipo.objects.all().count()
Equipo.objects.all().delete()
print(f"✅ {count} equipos eliminados")
print("Ahora puedes ejecutar: python manage.py makemigrations")
print("Y luego: python manage.py migrate")
