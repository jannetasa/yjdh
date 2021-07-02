# Generated by Django 3.2.3 on 2021-05-28 06:16

import uuid

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("contenttypes", "0002_remove_content_type_name"),
        ("oidc", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="EAuthorizationProfile",
            fields=[
                (
                    "id",
                    models.UUIDField(
                        default=uuid.uuid4,
                        editable=False,
                        primary_key=True,
                        serialize=False,
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="time created"
                    ),
                ),
                (
                    "modified_at",
                    models.DateTimeField(auto_now=True, verbose_name="time modified"),
                ),
                (
                    "id_token",
                    models.CharField(
                        blank=True, max_length=2048, verbose_name="id token"
                    ),
                ),
                (
                    "access_token",
                    models.CharField(
                        blank=True, max_length=2048, verbose_name="access token"
                    ),
                ),
                (
                    "access_token_expires",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="access token expires"
                    ),
                ),
                (
                    "refresh_token",
                    models.CharField(
                        blank=True, max_length=2048, verbose_name="refresh token"
                    ),
                ),
                (
                    "refresh_token_expires",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="refresh token expires"
                    ),
                ),
                (
                    "oidc_profile",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="eauthorization_profile",
                        to="oidc.oidcprofile",
                        verbose_name="oidc_profile",
                    ),
                ),
            ],
        ),
    ]