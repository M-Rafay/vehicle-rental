# Generated by Django 3.0 on 2021-12-03 18:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_auto_20211203_2158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='country',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='country', to='user.Country'),
        ),
    ]
