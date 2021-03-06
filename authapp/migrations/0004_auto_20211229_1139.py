# Generated by Django 3.2 on 2021-12-29 08:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0003_auto_20211225_2143'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopuserprofile',
            name='about_me',
            field=models.TextField(blank=True, max_length=512, null=True, verbose_name='Обо мне'),
        ),
        migrations.AlterField(
            model_name='shopuserprofile',
            name='gender',
            field=models.CharField(choices=[('M', 'М'), ('F', 'Ж'), ('U', 'Н')], default='U', max_length=1, verbose_name='Пол'),
        ),
        migrations.AlterField(
            model_name='shopuserprofile',
            name='tagline',
            field=models.CharField(blank=True, max_length=128, null=True, verbose_name='Тэги'),
        ),
    ]
