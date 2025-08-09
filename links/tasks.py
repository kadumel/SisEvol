from celery import shared_task
from time import sleep
from .models import Tarefa
from datetime import datetime
from django.utils import timezone
import subprocess
import os


@shared_task
def somar(i):
    sleep(20)  # Simula uma tarefa que demora 5 segundos
    Tarefa.objects.filter(id=i).update(status_processo='S', fim=timezone.now())
    return True


@shared_task
def executar_job_pentaho(id, path):
    # Caminho para a ferramenta Kitchen (dependendo do seu SO, você pode usar kitchen.bat ou kitchen.sh)
    # Atualize o caminho conforme o local do seu Pentaho
    
    caminho_sem_extensao, extensao = os.path.splitext(path)
    
    if extensao == '.kjb':
        pentaho_kitchen_path = os.path.join('C:\PDI\data-integration\Kitchen.bat')  # Altere para o caminho correto
    else:
        pentaho_kitchen_path = os.path.join('C:\PDI\data-integration\Pan.bat')  # Altere para o caminho correto
    

    # Caminho para o job do Pentaho
    caminho_job_pentaho = os.path.join(f'{path}')

    # Comando para executar o job
    comando = [pentaho_kitchen_path, '/file=' + caminho_job_pentaho + ' /logfile=C:/BI/Jobs/log/geral2.log /level=Detailed ']
    
    print(comando)

    # Execute o comando
    try:
        resultado = subprocess.run(comando, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        Tarefa.objects.filter(id=id).update(status_processo='S', fim=timezone.now())
        return resultado.stdout
    except subprocess.CalledProcessError as e:
        Tarefa.objects.filter(id=id).update(status_processo='F', fim=timezone.now())
        return f"Erro ao executar o job: {e.stderr.decode()}"
    
