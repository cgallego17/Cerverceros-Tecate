from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import HeroSlide, Patrocinador, CategoriaProducto, Producto, ItemFaq, Noticia, Jugador
from .panel_forms import (
    HeroSlideForm, PatrocinadorForm, CategoriaProductoForm,
    ProductoForm, ItemFaqForm, NoticiaForm, JugadorForm,
)

_LOGIN = '/panel/login/'



# ── AUTH ──────────────────────────────────────────

def panel_login(request):
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('panel:dashboard')
    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect(request.GET.get('next') or '/panel/')
        error = 'Credenciales incorrectas o sin permisos de acceso al panel.'
    return render(request, 'panel/login.html', {'error': error})


def panel_logout(request):
    logout(request)
    return redirect('panel:login')


# ── DASHBOARD ─────────────────────────────────────

@login_required(login_url=_LOGIN)
def dashboard(request):
    context = {
        'total_hero': HeroSlide.objects.count(),
        'total_patrocinadores': Patrocinador.objects.count(),
        'total_faq': ItemFaq.objects.count(),
        'total_productos': Producto.objects.count(),
        'total_categorias': CategoriaProducto.objects.count(),
        'total_noticias': Noticia.objects.count(),
        'total_jugadores': Jugador.objects.count(),
    }
    return render(request, 'panel/dashboard.html', context)


# ── HELPERS ───────────────────────────────────────

def _crud_form(request, FormClass, template, back_url, pk=None, msg_ok='Guardado correctamente.', extra_ctx=None):
    obj = get_object_or_404(FormClass.Meta.model, pk=pk) if pk else None
    form = FormClass(request.POST or None, request.FILES or None, instance=obj)
    if form.is_valid():
        form.save()
        messages.success(request, msg_ok)
        return redirect(back_url)
    ctx = {'form': form, 'objeto': obj, 'back_url': back_url}
    if extra_ctx:
        ctx.update(extra_ctx)
    return render(request, template, ctx)


def _crud_delete(request, ModelClass, back_url, pk, titulo='', msg_ok='Eliminado correctamente.'):
    obj = get_object_or_404(ModelClass, pk=pk)
    if request.method == 'POST':
        obj.delete()
        messages.success(request, msg_ok)
        return redirect(back_url)
    return render(request, 'panel/confirmar_eliminar.html', {
        'objeto': obj, 'back_url': back_url, 'titulo': titulo,
    })


# ── HERO SLIDES ───────────────────────────────────

@login_required(login_url=_LOGIN)
def hero_lista(request):
    return render(request, 'panel/hero_lista.html', {
        'slides': HeroSlide.objects.all(),
    })


@login_required(login_url=_LOGIN)
def hero_form(request, pk=None):
    return _crud_form(
        request, HeroSlideForm, 'panel/form.html', 'panel:hero_lista', pk,
        msg_ok='Diapositiva guardada.',
        extra_ctx={'titulo': 'Diapositiva Hero', 'back_url': 'panel:hero_lista'},
    )


@login_required(login_url=_LOGIN)
def hero_eliminar(request, pk):
    return _crud_delete(request, HeroSlide, 'panel:hero_lista', pk, 'Diapositiva Hero', 'Diapositiva eliminada.')


# ── PATROCINADORES ────────────────────────────────

@login_required(login_url=_LOGIN)
def patrocinadores_lista(request):
    return render(request, 'panel/patrocinadores_lista.html', {
        'patrocinadores': Patrocinador.objects.all(),
    })


@login_required(login_url=_LOGIN)
def patrocinador_form(request, pk=None):
    return _crud_form(
        request, PatrocinadorForm, 'panel/form.html', 'panel:patrocinadores_lista', pk,
        msg_ok='Patrocinador guardado.',
        extra_ctx={'titulo': 'Patrocinador', 'back_url': 'panel:patrocinadores_lista'},
    )


@login_required(login_url=_LOGIN)
def patrocinador_eliminar(request, pk):
    return _crud_delete(request, Patrocinador, 'panel:patrocinadores_lista', pk, 'Patrocinador', 'Patrocinador eliminado.')


# ── CATEGORÍAS ────────────────────────────────────

@login_required(login_url=_LOGIN)
def categorias_lista(request):
    return render(request, 'panel/categorias_lista.html', {
        'categorias': CategoriaProducto.objects.all(),
    })


@login_required(login_url=_LOGIN)
def categoria_form(request, pk=None):
    return _crud_form(
        request, CategoriaProductoForm, 'panel/form.html', 'panel:categorias_lista', pk,
        msg_ok='Categoría guardada.',
        extra_ctx={'titulo': 'Categoría de Producto', 'back_url': 'panel:categorias_lista'},
    )


@login_required(login_url=_LOGIN)
def categoria_eliminar(request, pk):
    return _crud_delete(request, CategoriaProducto, 'panel:categorias_lista', pk, 'Categoría', 'Categoría eliminada.')


# ── PRODUCTOS ─────────────────────────────────────

@login_required(login_url=_LOGIN)
def productos_lista(request):
    return render(request, 'panel/productos_lista.html', {
        'productos': Producto.objects.select_related('categoria').all(),
    })


@login_required(login_url=_LOGIN)
def producto_form(request, pk=None):
    return _crud_form(
        request, ProductoForm, 'panel/form.html', 'panel:productos_lista', pk,
        msg_ok='Producto guardado.',
        extra_ctx={'titulo': 'Producto', 'back_url': 'panel:productos_lista'},
    )


@login_required(login_url=_LOGIN)
def producto_eliminar(request, pk):
    return _crud_delete(request, Producto, 'panel:productos_lista', pk, 'Producto', 'Producto eliminado.')


# ── FAQ ───────────────────────────────────────────

@login_required(login_url=_LOGIN)
def faq_lista(request):
    return render(request, 'panel/faq_lista.html', {
        'items': ItemFaq.objects.all(),
    })


@login_required(login_url=_LOGIN)
def faq_form(request, pk=None):
    return _crud_form(
        request, ItemFaqForm, 'panel/form.html', 'panel:faq_lista', pk,
        msg_ok='Pregunta guardada.',
        extra_ctx={'titulo': 'Pregunta Frecuente', 'back_url': 'panel:faq_lista'},
    )


@login_required(login_url=_LOGIN)
def faq_eliminar(request, pk):
    return _crud_delete(request, ItemFaq, 'panel:faq_lista', pk, 'Pregunta Frecuente', 'Pregunta eliminada.')


# ── NOTICIAS ──────────────────────────────────────

@login_required(login_url=_LOGIN)
def noticias_lista(request):
    return render(request, 'panel/noticias_lista.html', {
        'noticias': Noticia.objects.all(),
    })


@login_required(login_url=_LOGIN)
def noticia_form(request, pk=None):
    return _crud_form(
        request, NoticiaForm, 'panel/form.html', 'panel:noticias_lista', pk,
        msg_ok='Noticia guardada.',
        extra_ctx={'titulo': 'Noticia', 'back_url': 'panel:noticias_lista'},
    )


@login_required(login_url=_LOGIN)
def noticia_eliminar(request, pk):
    return _crud_delete(request, Noticia, 'panel:noticias_lista', pk, 'Noticia', 'Noticia eliminada.')


# ── JUGADORES ─────────────────────────────────────

@login_required(login_url=_LOGIN)
def jugadores_lista(request):
    return render(request, 'panel/jugadores_lista.html', {
        'jugadores': Jugador.objects.all(),
    })


@login_required(login_url=_LOGIN)
def jugador_form(request, pk=None):
    return _crud_form(
        request, JugadorForm, 'panel/form.html', 'panel:jugadores_lista', pk,
        msg_ok='Jugador guardado.',
        extra_ctx={'titulo': 'Jugador', 'back_url': 'panel:jugadores_lista'},
    )


@login_required(login_url=_LOGIN)
def jugador_eliminar(request, pk):
    return _crud_delete(request, Jugador, 'panel:jugadores_lista', pk, 'Jugador', 'Jugador eliminado.')
