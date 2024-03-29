# Generated by Django 3.2.17 on 2023-02-08 19:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20230208_1717'),
    ]

    operations = [
        migrations.AlterField(
            model_name='section_workout',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='section_workout_fk', to='core.section'),
        ),
        migrations.CreateModel(
            name='Training_Section',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='training_section_fk', to='core.section')),
                ('training', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='training_fk', to='core.training')),
            ],
        ),
        migrations.AddField(
            model_name='training',
            name='sections',
            field=models.ManyToManyField(blank=True, related_name='training_section_mtm', through='core.Training_Section', to='core.Section'),
        ),
    ]
