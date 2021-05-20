# Generated by Django 3.2 on 2021-05-20 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('personas', '0004_alter_persona_img_persona'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='persona',
            name='apellido',
        ),
        migrations.RemoveField(
            model_name='persona',
            name='nombre',
        ),
        migrations.AddField(
            model_name='persona',
            name='nombre_apellido',
            field=models.CharField(default='', help_text='Nombre de la persona', max_length=100, verbose_name='Nombre'),
            preserve_default=False,
        ),
    ]
