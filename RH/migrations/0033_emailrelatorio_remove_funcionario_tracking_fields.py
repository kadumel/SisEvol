# Generated manually: EmailRelatorio + migração de dados + remoção em Funcionario

from django.db import migrations, models
import django.db.models.deletion


def copy_emails_from_funcionario(apps, schema_editor):
    Funcionario = apps.get_model("RH", "Funcionario")
    EmailRelatorio = apps.get_model("RH", "EmailRelatorio")
    seen = set()
    for f in Funcionario.objects.all().iterator():
        em = (getattr(f, "email_empresa", None) or "").strip()
        if not em:
            continue
        key = (f.empresa_id, em.lower())
        if key in seen:
            continue
        seen.add(key)
        rt = getattr(f, "relatorio_tracking", None) or "N"
        if rt not in ("S", "N"):
            rt = "N"
        EmailRelatorio.objects.get_or_create(
            empresa_id=f.empresa_id,
            email_empresa=em,
            defaults={"relatorio_tracking": rt},
        )


def noop_reverse(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ("RH", "0032_empresa_empresa_raiz"),
    ]

    operations = [
        migrations.CreateModel(
            name="EmailRelatorio",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "email_empresa",
                    models.CharField(max_length=100, verbose_name="E-mail"),
                ),
                (
                    "relatorio_tracking",
                    models.CharField(
                        choices=[("S", "SIM"), ("N", "NÃO")],
                        default="N",
                        max_length=1,
                        verbose_name="Receber relatório tracking",
                    ),
                ),
                (
                    "created",
                    models.DateTimeField(auto_now_add=True, null=True),
                ),
                (
                    "updated",
                    models.DateTimeField(auto_now=True, null=True),
                ),
                (
                    "empresa",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="emails_relatorio",
                        to="RH.empresa",
                        verbose_name="Empresa",
                    ),
                ),
            ],
            options={
                "verbose_name": "E-mail relatório tracking",
                "verbose_name_plural": "E-mails relatório tracking",
            },
        ),
        migrations.AddConstraint(
            model_name="emailrelatorio",
            constraint=models.UniqueConstraint(
                fields=("empresa", "email_empresa"),
                name="rh_emailrelatorio_empresa_email_uq",
            ),
        ),
        migrations.RunPython(copy_emails_from_funcionario, noop_reverse),
        migrations.RemoveField(
            model_name="funcionario",
            name="email_empresa",
        ),
        migrations.RemoveField(
            model_name="funcionario",
            name="relatorio_tracking",
        ),
    ]
