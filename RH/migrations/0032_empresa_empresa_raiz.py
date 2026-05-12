# Generated manually on 2026-05-12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RH', '0031_funcionario_email_empresa_funcionario_relatorio_tracking'),
    ]

    operations = [
        migrations.AddField(
            model_name='empresa',
            name='empresa_raiz',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
