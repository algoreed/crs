# Generated by Django 4.2.4 on 2023-08-27 11:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0001_initial"),
        ("community_benefit", "0003_alter_communitybenefitcategory_year_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="communitybenefitallocation",
            name="trust_region",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="community_benefit_allocations_by_trust_region",
                to="main.trustregion",
                verbose_name="Trust Region",
            ),
        ),
    ]
