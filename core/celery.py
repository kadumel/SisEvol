from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings

# Define o ambiente para as configurações do Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
os.environ.setdefault('FORKED_BY_MULTIPROCESSING', '1')

# Cria a instância do Celery
app = Celery('core')

# Defina o fuso horário para o Celery, garantindo que use o mesmo fuso horário do Django
app.conf.timezone = settings.TIME_ZONE
app.conf.enable_utc = False  # Desabilitar UTC (opcional, mas pode ajudar dependendo do seu caso)


# Usando uma string para o nome da fila evita problemas de importaçãos
# de Django e permite que o Celery se conecte diretamente com o Django.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Carrega tarefas de todos os módulos tasks.py em aplicativos registrados
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
