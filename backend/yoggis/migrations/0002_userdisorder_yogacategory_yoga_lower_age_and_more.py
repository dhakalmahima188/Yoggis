# Generated by Django 4.1.5 on 2023-01-11 16:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('yoggis', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserDisorder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=40)),
                ('description', models.TextField()),
                ('user_disorder_image', models.ImageField(upload_to='userDisorderImages/')),
            ],
        ),
        migrations.CreateModel(
            name='YogaCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(max_length=40)),
                ('description', models.TextField()),
                ('category_image', models.ImageField(upload_to='yogaCategoryImages/')),
            ],
        ),
        migrations.AddField(
            model_name='yoga',
            name='lower_age',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='yoga',
            name='upper_age',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='yoga',
            name='description',
            field=models.CharField(max_length=250),
        ),
        migrations.AlterField(
            model_name='yoga',
            name='image',
            field=models.ImageField(upload_to='yogaImages/'),
        ),
        migrations.CreateModel(
            name='CorrectVectorLocations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('angle_location', models.CharField(max_length=20)),
                ('angle_value', models.FloatField()),
                ('angle_of', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='yoggis.yoga')),
            ],
        ),
        migrations.AddField(
            model_name='yoga',
            name='avoid_for_disorder',
            field=models.ManyToManyField(to='yoggis.userdisorder'),
        ),
        migrations.AddField(
            model_name='yoga',
            name='yoga_category',
            field=models.ManyToManyField(to='yoggis.yogacategory'),
        ),
    ]
