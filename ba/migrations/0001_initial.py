# Generated by Django 4.1 on 2024-03-05 11:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Bean",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=20)),
                ("three_letters", models.CharField(max_length=3)),
                ("roast", models.IntegerField()),
                ("flavor", models.CharField(max_length=200)),
                ("acidity", models.CharField(max_length=100)),
                ("body", models.CharField(max_length=100)),
                ("processing", models.CharField(max_length=100)),
                ("region", models.CharField(max_length=100)),
                ("complementary", models.CharField(max_length=50)),
                ("is_promotion", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="QuestionSet",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="UserProfile",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_manager", models.BooleanField(default=False)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="userprofile",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Score",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("score", models.IntegerField(default=0)),
                ("times", models.IntegerField(default=0)),
                ("date", models.DateTimeField(auto_now_add=True)),
                ("count", models.IntegerField(default=0)),
                ("elapsed_time", models.DateTimeField(blank=True, null=True)),
                (
                    "question_set",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="ba.questionset"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Question",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.TextField()),
                ("explanation", models.TextField(blank=True, null=True)),
                ("is_multi", models.BooleanField(default=False)),
                (
                    "question_set",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="ba.questionset"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Option",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("text", models.CharField(max_length=255)),
                ("is_correct", models.BooleanField(default=False)),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="ba.question"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="FinalScore",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("score", models.IntegerField(default=0)),
                ("times", models.IntegerField(default=0)),
                ("date", models.DateTimeField(auto_now_add=True)),
                ("rate", models.IntegerField(default=0.0)),
                ("elapsed_time", models.CharField(default="00:00", max_length=10)),
                (
                    "question_set",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="ba.questionset"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Answer",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_correct", models.BooleanField(default=False)),
                (
                    "question",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="ba.question"
                    ),
                ),
                ("selected_options", models.ManyToManyField(to="ba.option")),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
