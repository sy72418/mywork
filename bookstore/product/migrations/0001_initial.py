# Generated by Django 4.1.3 on 2022-12-05 20:35

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="goods",
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
                ("title", models.CharField(max_length=150)),
                ("author", models.CharField(max_length=150)),
                ("publisher", models.CharField(max_length=150)),
                ("publish_date", models.DateField()),
                ("price", models.IntegerField()),
                ("img_url", models.CharField(max_length=250)),
                ("link_url", models.CharField(max_length=300)),
            ],
            options={"db_table": "goods",},
        ),
    ]
