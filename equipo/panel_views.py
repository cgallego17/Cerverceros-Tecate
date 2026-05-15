from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group, Permission
from django.contrib import messages
from django.db.models import Sum, Q
from django.utils import timezone
from itertools import groupby
from operator import attrgetter

from .models import HeroSlide, Patrocinador, CategoriaProducto, Producto, ItemFaq, Noticia, Jugador, Transaccion, Equipo, Partido
from .panel_forms import (
    HeroSlideForm, PatrocinadorForm, CategoriaProductoForm,
    ProductoForm, ItemFaqForm, NoticiaForm, JugadorForm,
    UsuarioCrearForm, UsuarioEditarForm, RolForm, TransaccionForm,
    EquipoForm, PartidoForm,
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
        'total_usuarios': User.objects.count(),
        'total_roles': Group.objects.count(),
        'total_transacciones': Transaccion.objects.count(),
        'balance_hoy': _caja_stats()['hoy']['balance'],
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


# ── USUARIOS ──────────────────────────────────────

def _superuser_check(request):
    """Returns True if the user is a superuser, otherwise redirects with error."""
    if not request.user.is_superuser:
        messages.error(request, 'Acceso denegado. Solo superusuarios pueden gestionar usuarios.')
        return False
    return True


@login_required(login_url=_LOGIN)
def usuarios_lista(request):
    if not _superuser_check(request):
        return redirect('panel:dashboard')
    usuarios = User.objects.all().order_by('-is_superuser', '-is_staff', 'username')
    return render(request, 'panel/usuarios_lista.html', {'usuarios': usuarios})


@login_required(login_url=_LOGIN)
def usuario_crear(request):
    if not _superuser_check(request):
        return redirect('panel:dashboard')
    form = UsuarioCrearForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        messages.success(request, f'Usuario "{form.cleaned_data["username"]}" creado correctamente.')
        return redirect('panel:usuarios_lista')
    return render(request, 'panel/usuario_form.html', {'form': form})


@login_required(login_url=_LOGIN)
def usuario_editar(request, pk):
    if not _superuser_check(request):
        return redirect('panel:dashboard')
    usuario = get_object_or_404(User, pk=pk)
    form = UsuarioEditarForm(request.POST or None, instance=usuario)
    if form.is_valid():
        user = form.save()
        # Keep current session valid if editing self
        if user == request.user:
            update_session_auth_hash(request, user)
        messages.success(request, f'Usuario "{user.username}" actualizado correctamente.')
        return redirect('panel:usuarios_lista')
    return render(request, 'panel/usuario_form.html', {'form': form, 'objeto': usuario})


@login_required(login_url=_LOGIN)
def usuario_eliminar(request, pk):
    if not _superuser_check(request):
        return redirect('panel:dashboard')
    usuario = get_object_or_404(User, pk=pk)
    if usuario == request.user:
        messages.error(request, 'No puedes eliminar tu propia cuenta.')
        return redirect('panel:usuarios_lista')
    if usuario.is_superuser:
        messages.error(request, 'No se puede eliminar una cuenta de superusuario.')
        return redirect('panel:usuarios_lista')
    if request.method == 'POST':
        nombre = usuario.username
        usuario.delete()
        messages.success(request, f'Usuario "{nombre}" eliminado correctamente.')
        return redirect('panel:usuarios_lista')
    return render(request, 'panel/confirmar_eliminar.html', {
        'objeto': usuario,
        'back_url': 'panel:usuarios_lista',
        'titulo': 'Usuario',
    })


# ── ROLES (Groups) ────────────────────────────────

def _permisos_agrupados():
    """Returns permissions for the equipo app grouped by content-type model."""
    perms = (
        Permission.objects
        .select_related('content_type')
        .filter(content_type__app_label='equipo')
        .order_by('content_type__model', 'codename')
    )
    groups = {}
    for perm in perms:
        label = perm.content_type.model.capitalize()
        groups.setdefault(label, []).append(perm)
    return groups


@login_required(login_url=_LOGIN)
def roles_lista(request):
    if not _superuser_check(request):
        return redirect('panel:dashboard')
    roles = Group.objects.prefetch_related('permissions', 'user_set').all().order_by('name')
    return render(request, 'panel/roles_lista.html', {'roles': roles})


@login_required(login_url=_LOGIN)
def rol_crear(request):
    if not _superuser_check(request):
        return redirect('panel:dashboard')
    form = RolForm(request.POST or None)
    if form.is_valid():
        rol = form.save()
        messages.success(request, f'Rol "{rol.name}" creado correctamente.')
        return redirect('panel:roles_lista')
    return render(request, 'panel/rol_form.html', {
        'form': form,
        'permisos_agrupados': _permisos_agrupados(),
    })


@login_required(login_url=_LOGIN)
def rol_editar(request, pk):
    if not _superuser_check(request):
        return redirect('panel:dashboard')
    rol = get_object_or_404(Group, pk=pk)
    form = RolForm(request.POST or None, instance=rol)
    if form.is_valid():
        form.save()
        messages.success(request, f'Rol "{rol.name}" actualizado correctamente.')
        return redirect('panel:roles_lista')
    return render(request, 'panel/rol_form.html', {
        'form': form,
        'objeto': rol,
        'permisos_agrupados': _permisos_agrupados(),
    })


@login_required(login_url=_LOGIN)
def rol_eliminar(request, pk):
    if not _superuser_check(request):
        return redirect('panel:dashboard')
    rol = get_object_or_404(Group, pk=pk)
    if request.method == 'POST':
        nombre = rol.name
        rol.delete()
        messages.success(request, f'Rol "{nombre}" eliminado correctamente.')
        return redirect('panel:roles_lista')
    return render(request, 'panel/confirmar_eliminar.html', {
        'objeto': rol,
        'back_url': 'panel:roles_lista',
        'titulo': 'Rol',
    })


# ── CAJA REGISTRADORA ─────────────────────────

def _staff_check(request):
    if not (request.user.is_staff or request.user.is_superuser):
        messages.error(request, 'No tienes permiso para acceder a esta sección.')
        return False
    return True


def _caja_stats():
    """Returns aggregated stats for today and current month."""
    hoy = timezone.now().date()
    mes_inicio = hoy.replace(day=1)

    def _agg(qs):
        r = qs.aggregate(
            ingresos=Sum('monto', filter=Q(tipo='ingreso')),
            egresos=Sum('monto',  filter=Q(tipo='egreso')),
        )
        ing = r['ingresos'] or 0
        egr = r['egresos']  or 0
        return {'ingresos': ing, 'egresos': egr, 'balance': ing - egr}

    return {
        'hoy':  _agg(Transaccion.objects.filter(fecha__date=hoy)),
        'mes':  _agg(Transaccion.objects.filter(fecha__date__gte=mes_inicio)),
        'total': _agg(Transaccion.objects.all()),
    }


@login_required(login_url=_LOGIN)
def caja_lista(request):
    if not _staff_check(request):
        return redirect('panel:dashboard')

    qs = Transaccion.objects.select_related('registrado_por').all()

    tipo      = request.GET.get('tipo', '')
    categoria = request.GET.get('categoria', '')
    metodo    = request.GET.get('metodo', '')
    fecha_desde = request.GET.get('fecha_desde', '')
    fecha_hasta = request.GET.get('fecha_hasta', '')

    if tipo:         qs = qs.filter(tipo=tipo)
    if categoria:    qs = qs.filter(categoria=categoria)
    if metodo:       qs = qs.filter(metodo_pago=metodo)
    if fecha_desde:  qs = qs.filter(fecha__date__gte=fecha_desde)
    if fecha_hasta:  qs = qs.filter(fecha__date__lte=fecha_hasta)

    stats = _caja_stats()

    return render(request, 'panel/caja_lista.html', {
        'transacciones':    qs,
        'stats':            stats,
        'tipo_actual':      tipo,
        'categoria_actual': categoria,
        'metodo_actual':    metodo,
        'fecha_desde':      fecha_desde,
        'fecha_hasta':      fecha_hasta,
        'TIPO_CHOICES':     Transaccion.TIPO_CHOICES,
        'CATEGORIA_CHOICES': Transaccion.CATEGORIA_CHOICES,
        'METODO_CHOICES':   Transaccion.METODO_CHOICES,
    })


@login_required(login_url=_LOGIN)
def transaccion_crear(request):
    if not _staff_check(request):
        return redirect('panel:dashboard')
    form = TransaccionForm(request.POST or None)
    if form.is_valid():
        t = form.save(commit=False)
        t.registrado_por = request.user
        t.save()
        messages.success(request, 'Transacción registrada correctamente.')
        return redirect('panel:caja_lista')
    return render(request, 'panel/transaccion_form.html', {'form': form})


@login_required(login_url=_LOGIN)
def transaccion_editar(request, pk):
    if not _staff_check(request):
        return redirect('panel:dashboard')
    transaccion = get_object_or_404(Transaccion, pk=pk)
    form = TransaccionForm(request.POST or None, instance=transaccion)
    # Pre-fill datetime-local field with current value
    if request.method == 'GET':
        form.initial['fecha'] = transaccion.fecha.strftime('%Y-%m-%dT%H:%M')
    if form.is_valid():
        form.save()
        messages.success(request, 'Transacción actualizada correctamente.')
        return redirect('panel:caja_lista')
    return render(request, 'panel/transaccion_form.html', {'form': form, 'objeto': transaccion})


@login_required(login_url=_LOGIN)
def transaccion_eliminar(request, pk):
    if not _staff_check(request):
        return redirect('panel:dashboard')
    transaccion = get_object_or_404(Transaccion, pk=pk)
    if request.method == 'POST':
        transaccion.delete()
        messages.success(request, 'Transacción eliminada correctamente.')
        return redirect('panel:caja_lista')
    return render(request, 'panel/confirmar_eliminar.html', {
        'objeto':   transaccion,
        'back_url': 'panel:caja_lista',
        'titulo':   'Transacción',
    })


# ── EQUIPOS ───────────────────────────────────────

@login_required(login_url=_LOGIN)
def equipos_lista(request):
    if not request.user.is_staff:
        return redirect('panel:dashboard')
    equipos = Equipo.objects.all().order_by('nombre')
    return render(request, 'panel/equipos_lista.html', {'equipos': equipos})


@login_required(login_url=_LOGIN)
def equipo_form(request, pk=None):
    if not request.user.is_staff:
        return redirect('panel:dashboard')
    equipo = get_object_or_404(Equipo, pk=pk) if pk else None
    form = EquipoForm(request.POST or None, request.FILES or None, instance=equipo)
    if form.is_valid():
        obj = form.save()
        messages.success(request, f'Equipo "{obj.nombre}" guardado correctamente.')
        return redirect('panel:equipos_lista')
    return render(request, 'panel/equipo_form.html', {'form': form, 'objeto': equipo})


@login_required(login_url=_LOGIN)
def equipo_eliminar(request, pk):
    if not request.user.is_staff:
        return redirect('panel:dashboard')
    equipo = get_object_or_404(Equipo, pk=pk)
    if request.method == 'POST':
        equipo.delete()
        messages.success(request, 'Equipo eliminado correctamente.')
        return redirect('panel:equipos_lista')
    return render(request, 'panel/confirmar_eliminar.html', {
        'objeto': equipo,
        'back_url': 'panel:equipos_lista',
        'titulo': 'Equipo',
    })


# ── PARTIDOS ──────────────────────────────────────

@login_required(login_url=_LOGIN)
def partidos_lista(request):
    if not request.user.is_staff:
        return redirect('panel:dashboard')
    partidos = Partido.objects.all().order_by('-fecha')
    return render(request, 'panel/partidos_lista.html', {'partidos': partidos})


@login_required(login_url=_LOGIN)
def partido_form(request, pk=None):
    if not request.user.is_staff:
        return redirect('panel:dashboard')
    partido = get_object_or_404(Partido, pk=pk) if pk else None
    form = PartidoForm(request.POST or None, instance=partido)
    if form.is_valid():
        obj = form.save()
        messages.success(request, f'Partido guardado correctamente.')
        return redirect('panel:partidos_lista')
    return render(request, 'panel/partido_form.html', {'form': form, 'objeto': partido})


@login_required(login_url=_LOGIN)
def partido_eliminar(request, pk):
    if not request.user.is_staff:
        return redirect('panel:dashboard')
    partido = get_object_or_404(Partido, pk=pk)
    if request.method == 'POST':
        partido.delete()
        messages.success(request, 'Partido eliminado correctamente.')
        return redirect('panel:partidos_lista')
    return render(request, 'panel/confirmar_eliminar.html', {
        'objeto': partido,
        'back_url': 'panel:partidos_lista',
        'titulo': 'Partido',
    })
