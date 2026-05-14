from django.core.management.base import BaseCommand
from equipo.models import (
    Producto, ArticuloNoticia, ImagenInstagram
)


class Command(BaseCommand):
    help = 'Agrega URLs de imágenes placeholder a todos los modelos'

    def handle(self, *args, **kwargs):
        self.stdout.write('Agregando imágenes placeholder...\n')

        # Productos
        self.stdout.write('- Productos...')
        productos = Producto.objects.filter(destacado=True)
        imagenes_productos = [
            "https://placehold.co/400x400/1a1a1a/e31e24?text=Jersey+Oficial+(400x400)",
            "https://placehold.co/400x400/2a2a2a/e31e24?text=Gorra+Roja+(400x400)",
            "https://placehold.co/400x400/1a1a1a/e31e24?text=Playera+(400x400)",
            "https://placehold.co/400x400/2a2a2a/e31e24?text=Sudadera+(400x400)",
            "https://placehold.co/400x400/1a1a1a/e31e24?text=Balon+(400x400)",
            "https://placehold.co/400x400/2a2a2a/e31e24?text=Taza+(400x400)",
            "https://placehold.co/400x400/1a1a1a/e31e24?text=Chamarra+(400x400)",
            "https://placehold.co/400x400/2a2a2a/e31e24?text=Llavero+(400x400)",
        ]
        
        for i, producto in enumerate(productos):
            if i < len(imagenes_productos):
                producto.descripcion = f"{producto.nombre}\n\nImagen: {imagenes_productos[i]}"
                producto.save()
                self.stdout.write(f"  - {producto.nombre}: {imagenes_productos[i]}")

        # Artículos de Noticias (solo los de tipo imagen)
        self.stdout.write('\n- Artículos de noticias (tipo imagen)...')
        articulos_imagen = ArticuloNoticia.objects.filter(tipo='imagen', destacado_grid=True)
        imagenes_noticias = [
            "https://placehold.co/600x400/1a1a1a/e31e24?text=Noticia+1+(600x400)",
            "https://placehold.co/600x400/2a2a2a/e31e24?text=Noticia+2+(600x400)",
            "https://placehold.co/600x400/1a1a1a/e31e24?text=Noticia+3+(600x400)",
            "https://placehold.co/600x400/2a2a2a/e31e24?text=Noticia+4+(600x400)",
        ]
        
        for i, articulo in enumerate(articulos_imagen):
            if i < len(imagenes_noticias):
                articulo.descripcion = f"Imagen: {imagenes_noticias[i]}"
                articulo.save()
                self.stdout.write(f"  - {articulo.titulo}: {imagenes_noticias[i]}")

        # Imágenes de Instagram
        self.stdout.write('\n- Imágenes de Instagram...')
        ImagenInstagram.objects.all().delete()
        imagenes_ig = [
            "https://placehold.co/600x600/1a1a1a/e31e24?text=Instagram+1+(600x600)",
            "https://placehold.co/600x600/2a2a2a/e31e24?text=Instagram+2+(600x600)",
            "https://placehold.co/600x600/1a1a1a/e31e24?text=Instagram+3+(600x600)",
            "https://placehold.co/600x600/2a2a2a/e31e24?text=Instagram+4+(600x600)",
        ]
        
        for i, url in enumerate(imagenes_ig, 1):
            ImagenInstagram.objects.create(
                imagen_url=url,
                enlace="https://instagram.com/cerveceros",
                orden=i,
                activo=True
            )
            self.stdout.write(f"  - Instagram {i}: {url}")

        self.stdout.write(self.style.SUCCESS('\n✓ URLs de imágenes placeholder agregadas!'))
        self.stdout.write(self.style.WARNING('\nNOTA: Las imágenes placeholder son URLs externas.'))
        self.stdout.write(self.style.WARNING('Para ver las imágenes en los productos y artículos,'))
        self.stdout.write(self.style.WARNING('revisa el campo "Descripción" donde están las URLs.'))
        self.stdout.write(self.style.WARNING('\nPara Instagram, necesitas subir las imágenes manualmente desde:'))
        for i, url in enumerate(imagenes_ig, 1):
            self.stdout.write(f'  {i}. {url}')
