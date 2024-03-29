# Generated by Django 4.2.4 on 2023-08-27 13:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("community_context", "0005_alter_dwelling_dwelling_number"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="householdbankaccount",
            options={
                "verbose_name": "Household Bank Account",
                "verbose_name_plural": "Household Bank Accounts",
            },
        ),
        migrations.AddField(
            model_name="householdbankaccount",
            name="status",
            field=models.CharField(
                blank=True,
                choices=[("Active", "Active"), ("Dormant", "Dormant"), ("NA", "NA")],
                max_length=10,
                verbose_name="Status",
            ),
        ),
    ]
