"""
Tarefas executadas em segundo plano pelo Django-Q2.

Com django-q2 não é necessário decorador — as funções são simplesmente
referenciadas pelo caminho completo (string) ao chamar `async_task(...)`.
Para executar o worker:

    python manage.py qcluster
"""

from time import sleep
from datetime import datetime
from django.utils import timezone
import subprocess
import os

from .models import Tarefa


def somar(i):
    sleep(20)
    Tarefa.objects.filter(id=i).update(status_processo='S', fim=timezone.now())
    return True


def executar_job_pentaho(id, path):
    caminho_sem_extensao, extensao = os.path.splitext(path)

    if extensao == '.kjb':
        pentaho_kitchen_path = os.path.join('C:\\PDI\\data-integration\\Kitchen.bat')
    else:
        pentaho_kitchen_path = os.path.join('C:\\PDI\\data-integration\\Pan.bat')

    caminho_job_pentaho = os.path.join(f'{path}')

    comando = [
        pentaho_kitchen_path,
        '/file=' + caminho_job_pentaho + ' /logfile=C:/BI/Jobs/log/geral2.log /level=Detailed ',
    ]

    print(comando)

    try:
        resultado = subprocess.run(
            comando, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        Tarefa.objects.filter(id=id).update(status_processo='S', fim=timezone.now())
        return resultado.stdout
    except subprocess.CalledProcessError as e:
        Tarefa.objects.filter(id=id).update(status_processo='F', fim=timezone.now())
        return f"Erro ao executar o job: {e.stderr.decode()}"
