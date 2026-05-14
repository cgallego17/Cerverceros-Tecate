from django import forms
from .models import HeroSlide, Patrocinador, CategoriaProducto, Producto, ItemFaq, Noticia, Jugador

_i = {'class': 'panel-input'}
_ta = {'class': 'panel-textarea', 'rows': 5}
_sel = {'class': 'panel-select'}


class HeroSlideForm(forms.ModelForm):
    class Meta:
        model = HeroSlide
        fields = [
            'subtitulo', 'titulo_linea1', 'titulo_linea2',
            'imagen', 'imagen_url',
            'btn1_texto', 'btn1_url', 'btn2_texto', 'btn2_url',
            'orden', 'activo',
        ]
        widgets = {
            'subtitulo': forms.TextInput(attrs=_i),
            'titulo_linea1': forms.TextInput(attrs=_i),
            'titulo_linea2': forms.TextInput(attrs=_i),
            'imagen_url': forms.URLInput(attrs=_i),
            'btn1_texto': forms.TextInput(attrs=_i),
            'btn1_url': forms.TextInput(attrs=_i),
            'btn2_texto': forms.TextInput(attrs=_i),
            'btn2_url': forms.TextInput(attrs=_i),
            'orden': forms.NumberInput(attrs=_i),
        }


class PatrocinadorForm(forms.ModelForm):
    class Meta:
        model = Patrocinador
        fields = ['nombre', 'logo', 'url', 'orden', 'activo']
        widgets = {
            'nombre': forms.TextInput(attrs=_i),
            'url': forms.URLInput(attrs=_i),
            'orden': forms.NumberInput(attrs=_i),
        }


class CategoriaProductoForm(forms.ModelForm):
    class Meta:
        model = CategoriaProducto
        fields = ['nombre']
        widgets = {
            'nombre': forms.TextInput(attrs=_i),
        }


class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = [
            'nombre', 'descripcion', 'categoria', 'imagen',
            'precio', 'precio_anterior', 'badge', 'activo', 'destacado',
        ]
        widgets = {
            'nombre': forms.TextInput(attrs=_i),
            'descripcion': forms.Textarea(attrs=_ta),
            'categoria': forms.Select(attrs=_sel),
            'precio': forms.NumberInput(attrs={**_i, 'step': '0.01'}),
            'precio_anterior': forms.NumberInput(attrs={**_i, 'step': '0.01'}),
            'badge': forms.Select(attrs=_sel),
        }


class ItemFaqForm(forms.ModelForm):
    class Meta:
        model = ItemFaq
        fields = ['titulo', 'contenido', 'orden', 'activo']
        widgets = {
            'titulo': forms.TextInput(attrs=_i),
            'contenido': forms.Textarea(attrs=_ta),
            'orden': forms.NumberInput(attrs=_i),
        }


class NoticiaForm(forms.ModelForm):
    class Meta:
        model = Noticia
        fields = ['titulo', 'contenido', 'imagen', 'autor', 'destacada']
        widgets = {
            'titulo': forms.TextInput(attrs=_i),
            'contenido': forms.Textarea(attrs={**_ta, 'rows': 8}),
            'autor': forms.TextInput(attrs=_i),
        }


class JugadorForm(forms.ModelForm):
    class Meta:
        model = Jugador
        fields = [
            'nombre', 'numero', 'posicion', 'foto', 'biografia',
            'fecha_nacimiento', 'altura', 'peso', 'bateo', 'lanzamiento',
            'activo', 'destacado_inicio',
        ]
        widgets = {
            'nombre': forms.TextInput(attrs=_i),
            'numero': forms.NumberInput(attrs=_i),
            'posicion': forms.Select(attrs=_sel),
            'biografia': forms.Textarea(attrs=_ta),
            'fecha_nacimiento': forms.DateInput(attrs={**_i, 'type': 'date'}),
            'altura': forms.TextInput(attrs=_i),
            'peso': forms.TextInput(attrs=_i),
            'bateo': forms.TextInput(attrs=_i),
            'lanzamiento': forms.TextInput(attrs=_i),
        }
