# Generated by Django 4.1.5 on 2023-01-28 05:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('yoggis', '0008_yogascore_yoga'),
    ]

    operations = [
        migrations.AlterField(
            model_name='yogascore',
            name='yoga',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='yogaOwner', to='yoggis.yoga'),
        ),
    ]
