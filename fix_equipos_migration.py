#!/usr/bin/env python
"""
Script para limpiar equipos y partidos antes de migrar campo ciudad a ForeignKey
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cerveceros_tecate.settings')
django.setup()

from django.db import connection

# Usar SQL directo para eliminar datos
with connection.cursor() as cursor:
    # Desactivar restricciones de clave foránea temporalmente
    cursor.execute("PRAGMA foreign_keys = OFF")
    
    # Eliminar boletos que referencian partidos
    cursor.execute("DELETE FROM equipo_boleto")
    boletos_count = cursor.rowcount
    
    # Eliminar tabla de posiciones que referencia equipos
    cursor.execute("DELETE FROM equipo_tablaposiciones")
    posiciones_count = cursor.rowcount
    
    # Eliminar partidos que referencian equipos
    cursor.execute("DELETE FROM equipo_partido")
    partidos_count = cursor.rowcount
    
    # Eliminar equipos
    cursor.execute("DELETE FROM equipo_equipo")
    equipos_count = cursor.rowcount
    
    # Reactivar restricciones de clave foránea
    cursor.execute("PRAGMA foreign_keys = ON")
    
print(f"✅ {boletos_count} boletos eliminados")
print(f"✅ {posiciones_count} posiciones eliminadas")
print(f"✅ {partidos_count} partidos eliminados")
print(f"✅ {equipos_count} equipos eliminados")
print("\nAhora ejecuta:")
print("  python manage.py migrate")
