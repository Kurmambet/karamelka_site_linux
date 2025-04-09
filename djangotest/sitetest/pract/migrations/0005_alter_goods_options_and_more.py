# Generated by Django 5.1.7 on 2025-03-17 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pract', '0004_alter_goods_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='goods',
            options={'ordering': ['time_create']},
        ),
        migrations.RemoveIndex(
            model_name='goods',
            name='pract_goods_time_cr_887f4d_idx',
        ),
        migrations.RemoveField(
            model_name='goods',
            name='is_published',
        ),
        migrations.AddField(
            model_name='goods',
            name='is_stock',
            field=models.BooleanField(choices=[(0, 'Нет в наличии'), (1, 'Есть в наличии')], default=1),
        ),
        migrations.AddIndex(
            model_name='goods',
            index=models.Index(fields=['time_create'], name='pract_goods_time_cr_2d8c5b_idx'),
        ),
    ]
