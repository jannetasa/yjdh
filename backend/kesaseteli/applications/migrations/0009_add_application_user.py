# Generated by Django 3.2.4 on 2021-08-30 09:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("applications", "0008_delete_applications"),
    ]

    operations = [
        migrations.AddField(
            model_name="application",
            name="user",
            field=models.ForeignKey(
                default=None,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="applications",
                to="auth.user",
                verbose_name="user",
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="historicalapplication",
            name="user",
            field=models.ForeignKey(
                blank=True,
                db_constraint=False,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="+",
                to=settings.AUTH_USER_MODEL,
                verbose_name="user",
            ),
        ),
    ]