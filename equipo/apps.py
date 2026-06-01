from django.apps import AppConfig


class EquipoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'equipo'

    def ready(self):
        # Pre-carga las imágenes de Instagram en segundo plano al arrancar
        from equipo.context_processors import warm_cache
        warm_cache()
