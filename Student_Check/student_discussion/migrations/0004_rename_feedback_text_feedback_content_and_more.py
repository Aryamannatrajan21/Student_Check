# Generated by Django 5.1.1 on 2024-11-14 06:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("student_discussion", "0003_professor_feedback"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name="feedback",
            old_name="feedback_text",
            new_name="content",
        ),
        migrations.RenameField(
            model_name="feedback",
            old_name="timestamp",
            new_name="created_at",
        ),
        migrations.AlterField(
            model_name="feedback",
            name="professor",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="student_discussion.professor",
            ),
        ),
        migrations.AlterField(
            model_name="feedback",
            name="student",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
