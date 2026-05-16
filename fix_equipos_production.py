#!/usr/bin/env python
"""
Script para limpiar equipos y datos relacionados antes de migrar campo ciudad a ForeignKey
Compatible con SQLite (desarrollo) y PostgreSQL (producción)
"""

import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cerveceros_tecate.settings')
django.setup()

from django.db import connection

def limpiar_datos():
    """Elimina todos los datos relacionados con equipos y partidos"""
    
    # Detectar tipo de base de datos
    db_vendor = connection.vendor
    print(f"📊 Base de datos detectada: {db_vendor}")
    
    with connection.cursor() as cursor:
        if db_vendor == 'sqlite':
            # SQLite: Desactivar restricciones de clave foránea
            cursor.execute("PRAGMA foreign_keys = OFF")
        
        try:
            # Eliminar en orden para evitar conflictos de FK
            tablas = [
                ('equipo_boleto', 'boletos'),
                ('equipo_tablaposiciones', 'posiciones'),
                ('equipo_partido', 'partidos'),
                ('equipo_equipo', 'equipos'),
            ]
            
            resultados = {}
            for tabla, nombre in tablas:
                try:
                    cursor.execute(f"DELETE FROM {tabla}")
                    count = cursor.rowcount
                    resultados[nombre] = count
                    print(f"✅ {count} {nombre} eliminados")
                except Exception as e:
                    print(f"⚠️  Error eliminando {nombre}: {e}")
                    resultados[nombre] = 0
            
            if db_vendor == 'sqlite':
                # SQLite: Reactivar restricciones
                cursor.execute("PRAGMA foreign_keys = ON")
            
            # Confirmar transacción
            connection.commit()
            
            print("\n" + "="*50)
            print("✅ Limpieza completada exitosamente")
            print("="*50)
            print(f"Total eliminado:")
            for nombre, count in resultados.items():
                print(f"  - {count} {nombre}")
            
            print("\n📝 Siguiente paso:")
            print("  En el servidor, ejecuta:")
            print("    cd /home/deploy/cerveceros_tecate")
            print("    source venv/bin/activate")
            print("    python manage.py migrate")
            
            return True
            
        except Exception as e:
            print(f"\n❌ Error durante la limpieza: {e}")
            connection.rollback()
            return False

if __name__ == '__main__':
    print("🧹 Iniciando limpieza de datos...")
    print("⚠️  ADVERTENCIA: Esto eliminará todos los equipos, partidos, boletos y posiciones")
    print()
    
    if '--confirm' not in sys.argv:
        respuesta = input("¿Estás seguro de continuar? (escribe 'SI' para confirmar): ")
        if respuesta != 'SI':
            print("❌ Operación cancelada")
            sys.exit(1)
    
    exito = limpiar_datos()
    sys.exit(0 if exito else 1)
