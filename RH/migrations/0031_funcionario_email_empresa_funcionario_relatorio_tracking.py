# Generated manually on 2026-05-11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('RH', '0030_operacao_empresa_operacao'),
    ]

    operations = [
        migrations.AddField(
            model_name='funcionario',
            name='email_empresa',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='E-mail Empresa'),
        ),
        migrations.AddField(
            model_name='funcionario',
            name='relatorio_tracking',
            field=models.CharField(
                blank=True,
                choices=[('S', 'SIM'), ('N', 'NÃO')],
                default='N',
                max_length=1,
                null=True,
                verbose_name='Receber Relatório Tracking',
            ),
        ),
    ]
