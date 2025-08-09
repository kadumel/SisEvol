from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        """
        Executado quando o Django inicia
        """
        # Importar e aplicar a configuração de date_hierarchy
        try:
            from .admin_config import apply_date_hierarchy_mixin
            apply_date_hierarchy_mixin()
        except ImportError:
            # Se o arquivo não existir, não fazer nada
            pass 