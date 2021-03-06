# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2020-05-30 22:19
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, verbose_name='Назва дошки')),
            ],
        ),
        migrations.CreateModel(
            name='Domain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(max_length=140)),
                ('admin', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='domains', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_approved', models.BooleanField(default=False)),
                ('level', models.CharField(choices=[('J', 'Початковий'), ('M', 'Середнiй'), ('S', 'Старший')], default='J', max_length=1)),
                ('is_main_operator', models.BooleanField(default=False)),
                ('domain', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='profiles', to='todo.Domain')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Todo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=140, verbose_name='Титульна завдання')),
                ('task', models.TextField(max_length=255, verbose_name='Умова завдання')),
                ('status', models.CharField(choices=[('A', 'Активна'), ('P', 'Очікує на розгляд'), ('D', 'Завершена'), ('C', 'Відмінено')], default='A', max_length=1, verbose_name='Статус завдання')),
                ('priority', models.CharField(choices=[('L', '😌 Низький'), ('S', '😀 Стандартний'), ('H', '🔥 Високий')], default='S', max_length=1, verbose_name='Пріоритет')),
                ('image', models.ImageField(blank=True, null=True, upload_to='', verbose_name='Скрiншот показника')),
                ('temperature', models.IntegerField(blank=True, default=0, null=True, verbose_name='Температура котельнi')),
                ('heat_meter', models.IntegerField(blank=True, default=0, null=True, verbose_name='Лічильник тепла')),
                ('water_leak', models.BooleanField(default=False, verbose_name='Витік води')),
                ('flooding', models.BooleanField(default=False, verbose_name='Затоплення')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Створена')),
                ('deadline', models.DateField(blank=True, default=datetime.datetime(2020, 5, 30, 22, 19, 26, 683544, tzinfo=utc), null=True, verbose_name='Кінцева дата')),
                ('time', models.PositiveSmallIntegerField(blank=True, default=0, null=True, verbose_name='Часи на виконання')),
                ('assignee', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assigned', to=settings.AUTH_USER_MODEL, verbose_name='Виконавець')),
                ('assignor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assignor', to=settings.AUTH_USER_MODEL, verbose_name='Створювач')),
                ('board', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='todo.Board', verbose_name='Дошка')),
            ],
        ),
        migrations.CreateModel(
            name='TypeBoiler',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Назва котельной')),
                ('year', models.PositiveIntegerField(default=2000, verbose_name='Рiк випуску')),
            ],
        ),
    ]
