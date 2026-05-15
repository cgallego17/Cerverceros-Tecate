#!/usr/bin/env python
"""
Script para poblar México con sus estados y ciudades principales
Uso: python poblar_mexico.py
"""

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cerveceros_tecate.settings')
django.setup()

from equipo.models import Pais, Estado, Ciudad

def poblar_mexico():
    print("🇲🇽 Poblando México con estados y ciudades...")
    
    # Crear o obtener México
    mexico, created = Pais.objects.get_or_create(
        codigo='MEX',
        defaults={'nombre': 'México', 'activo': True}
    )
    if created:
        print(f"✅ País creado: {mexico.nombre}")
    else:
        print(f"ℹ️  País ya existe: {mexico.nombre}")
    
    # Estados y sus ciudades principales
    estados_ciudades = {
        'Aguascalientes': ['Aguascalientes', 'Calvillo', 'Jesús María'],
        'Baja California': ['Tijuana', 'Mexicali', 'Ensenada', 'Tecate', 'Rosarito'],
        'Baja California Sur': ['La Paz', 'Los Cabos', 'San José del Cabo'],
        'Campeche': ['Campeche', 'Ciudad del Carmen'],
        'Chiapas': ['Tuxtla Gutiérrez', 'San Cristóbal de las Casas', 'Tapachula'],
        'Chihuahua': ['Chihuahua', 'Ciudad Juárez', 'Delicias'],
        'Coahuila': ['Saltillo', 'Torreón', 'Monclova', 'Piedras Negras'],
        'Colima': ['Colima', 'Manzanillo', 'Tecomán'],
        'Ciudad de México': ['Ciudad de México'],
        'Durango': ['Durango', 'Gómez Palacio'],
        'Guanajuato': ['León', 'Guanajuato', 'Celaya', 'Irapuato', 'Salamanca'],
        'Guerrero': ['Acapulco', 'Chilpancingo', 'Zihuatanejo', 'Taxco'],
        'Hidalgo': ['Pachuca', 'Tulancingo', 'Tula'],
        'Jalisco': ['Guadalajara', 'Zapopan', 'Tlaquepaque', 'Puerto Vallarta', 'Tonalá'],
        'Estado de México': ['Toluca', 'Ecatepec', 'Naucalpan', 'Nezahualcóyotl'],
        'Michoacán': ['Morelia', 'Uruapan', 'Zamora', 'Lázaro Cárdenas'],
        'Morelos': ['Cuernavaca', 'Cuautla', 'Jiutepec'],
        'Nayarit': ['Tepic', 'Bahía de Banderas'],
        'Nuevo León': ['Monterrey', 'Guadalupe', 'San Pedro Garza García', 'Apodaca', 'San Nicolás de los Garza'],
        'Oaxaca': ['Oaxaca', 'Salina Cruz', 'Juchitán'],
        'Puebla': ['Puebla', 'Tehuacán', 'Cholula'],
        'Querétaro': ['Querétaro', 'San Juan del Río'],
        'Quintana Roo': ['Cancún', 'Chetumal', 'Playa del Carmen', 'Cozumel', 'Tulum'],
        'San Luis Potosí': ['San Luis Potosí', 'Soledad de Graciano Sánchez'],
        'Sinaloa': ['Culiacán', 'Mazatlán', 'Los Mochis', 'Guasave'],
        'Sonora': ['Hermosillo', 'Nogales', 'Ciudad Obregón', 'Guaymas'],
        'Tabasco': ['Villahermosa', 'Cárdenas', 'Comalcalco'],
        'Tamaulipas': ['Reynosa', 'Matamoros', 'Tampico', 'Ciudad Victoria', 'Nuevo Laredo'],
        'Tlaxcala': ['Tlaxcala', 'Apizaco'],
        'Veracruz': ['Veracruz', 'Xalapa', 'Coatzacoalcos', 'Córdoba', 'Poza Rica'],
        'Yucatán': ['Mérida', 'Valladolid', 'Progreso'],
        'Zacatecas': ['Zacatecas', 'Fresnillo'],
    }
    
    total_estados = 0
    total_ciudades = 0
    
    for nombre_estado, ciudades in estados_ciudades.items():
        # Crear o obtener estado
        estado, created = Estado.objects.get_or_create(
            pais=mexico,
            nombre=nombre_estado,
            defaults={'activo': True}
        )
        if created:
            total_estados += 1
            print(f"  ✅ Estado creado: {nombre_estado}")
        
        # Crear ciudades
        for nombre_ciudad in ciudades:
            ciudad, created = Ciudad.objects.get_or_create(
                estado=estado,
                nombre=nombre_ciudad,
                defaults={'activo': True}
            )
            if created:
                total_ciudades += 1
    
    print(f"\n🎉 Proceso completado:")
    print(f"   📍 {total_estados} estados creados")
    print(f"   🏙️  {total_ciudades} ciudades creadas")
    print(f"\n✅ México poblado exitosamente con {Estado.objects.filter(pais=mexico).count()} estados")
    print(f"   y {Ciudad.objects.filter(estado__pais=mexico).count()} ciudades en total")

if __name__ == '__main__':
    poblar_mexico()
