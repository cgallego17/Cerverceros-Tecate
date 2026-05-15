from django import forms
from django.contrib.auth.models import User, Group, Permission
from django.contrib.auth.password_validation import validate_password
from django.utils import timezone
from .models import HeroSlide, Patrocinador, CategoriaProducto, Producto, ItemFaq, Noticia, Jugador, Transaccion, Equipo, Partido

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


# ── USUARIOS ──────────────────────────────────────

class UsuarioCrearForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Contraseña',
        widget=forms.PasswordInput(attrs=_i),
    )
    password2 = forms.CharField(
        label='Confirmar contraseña',
        widget=forms.PasswordInput(attrs=_i),
    )
    
    avatar = forms.ImageField(
        label='Foto de perfil',
        required=False,
        widget=forms.FileInput(attrs={'class': 'panel-input', 'accept': 'image/*'}),
    )

    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Roles asignados',
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'groups']
        widgets = {
            'username':   forms.TextInput(attrs=_i),
            'first_name': forms.TextInput(attrs=_i),
            'last_name':  forms.TextInput(attrs=_i),
            'email':      forms.EmailInput(attrs=_i),
        }

    def clean_password2(self):
        p1 = self.cleaned_data.get('password1', '')
        p2 = self.cleaned_data.get('password2', '')
        if p1 != p2:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        if p1:
            validate_password(p1)
        return p2

    def save(self, commit=True):
        from .models import UserProfile
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            user.groups.set(self.cleaned_data.get('groups', []))
            
            # Crear perfil con avatar si se proporcionó
            avatar = self.cleaned_data.get('avatar')
            if avatar:
                UserProfile.objects.create(user=user, avatar=avatar)
            else:
                UserProfile.objects.create(user=user)
        return user


class UsuarioEditarForm(forms.ModelForm):
    password1 = forms.CharField(
        label='Nueva contraseña (dejar vacío para no cambiar)',
        widget=forms.PasswordInput(attrs=_i),
        required=False,
    )
    password2 = forms.CharField(
        label='Confirmar nueva contraseña',
        widget=forms.PasswordInput(attrs=_i),
        required=False,
    )
    groups = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Roles asignados',
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_staff', 'is_active', 'groups']
        widgets = {
            'username':   forms.TextInput(attrs=_i),
            'first_name': forms.TextInput(attrs=_i),
            'last_name':  forms.TextInput(attrs=_i),
            'email':      forms.EmailInput(attrs=_i),
        }

    def clean(self):
        cleaned = super().clean()
        p1 = cleaned.get('password1', '')
        p2 = cleaned.get('password2', '')
        if p1 or p2:
            if p1 != p2:
                raise forms.ValidationError('Las contraseñas no coinciden.')
            validate_password(p1)
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        p = self.cleaned_data.get('password1')
        if p:
            user.set_password(p)
        if commit:
            user.save()
            self.save_m2m()
        return user


# ── ROLES (Groups) ────────────────────────────────

class RolForm(forms.ModelForm):
    permissions = forms.ModelMultipleChoiceField(
        queryset=Permission.objects.select_related('content_type').filter(
            content_type__app_label='equipo'
        ).order_by('content_type__model', 'codename'),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label='Permisos',
    )

    class Meta:
        model = Group
        fields = ['name', 'permissions']
        widgets = {
            'name': forms.TextInput(attrs=_i),
        }


# ── CAJA REGISTRADORA ─────────────────────────

class TransaccionForm(forms.ModelForm):
    fecha = forms.DateTimeField(
        label='Fecha y hora',
        widget=forms.DateTimeInput(
            attrs={**_i, 'type': 'datetime-local'},
            format='%Y-%m-%dT%H:%M',
        ),
        input_formats=['%Y-%m-%dT%H:%M'],
        initial=timezone.now,
    )

    class Meta:
        model = Transaccion
        fields = ['concepto', 'tipo', 'categoria', 'monto', 'metodo_pago', 'fecha', 'notas']
        widgets = {
            'concepto':   forms.TextInput(attrs=_i),
            'tipo':       forms.Select(attrs=_sel),
            'categoria':  forms.Select(attrs=_sel),
            'monto':      forms.NumberInput(attrs={**_i, 'step': '0.01', 'min': '0.01'}),
            'metodo_pago': forms.Select(attrs=_sel),
            'notas':      forms.Textarea(attrs={**_ta, 'rows': 3}),
        }


class EquipoForm(forms.ModelForm):
    class Meta:
        model = Equipo
        fields = ['nombre', 'ciudad', 'logo']
        widgets = {
            'nombre': forms.TextInput(attrs=_i),
            'ciudad': forms.TextInput(attrs=_i),
        }


class PartidoForm(forms.ModelForm):
    fecha = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={**_i, 'type': 'datetime-local'}),
        label='Fecha y hora'
    )
    
    class Meta:
        model = Partido
        fields = ['fecha', 'equipo_local', 'equipo_visitante', 'carreras_local', 'carreras_visitante', 'estado', 'estadio', 'temporada']
        widgets = {
            'equipo_local': forms.Select(attrs=_sel),
            'equipo_visitante': forms.Select(attrs=_sel),
            'carreras_local': forms.NumberInput(attrs={**_i, 'min': '0'}),
            'carreras_visitante': forms.NumberInput(attrs={**_i, 'min': '0'}),
            'estado': forms.Select(attrs=_sel),
            'estadio': forms.TextInput(attrs=_i),
            'temporada': forms.TextInput(attrs=_i),
        }
