# Generated by Django 4.2.10 on 2024-03-04 14:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("consumer", "0003_rename_profile_catchpyprofile"),
    ]

    operations = [
        migrations.AlterField(
            model_name="catchpyprofile",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="catchpy_profile",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
