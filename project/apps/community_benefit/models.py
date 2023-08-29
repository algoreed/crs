from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from datetime import datetime, date
from apps.main.models import TrustRegion, TrustVillage, Bank

# Create your models here.


class CommunityBenefitCategory(models.Model):
    name = models.CharField("Name", max_length=255)
    trust_region = models.ForeignKey(
        TrustRegion,
        on_delete=models.SET_NULL,
        null=True,
        related_name="community_benefits_by_trust_region",
        verbose_name="Trust Region",
    )
    year = models.PositiveIntegerField(
        "Year",
        null=True,
        validators=[MinValueValidator(1900), MaxValueValidator(datetime.now().year)],
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Community Benefit Category"
        verbose_name_plural = "Community Benefit Categories"


class CommunityBenefitAllocation(models.Model):
    community_benefit_category = models.ForeignKey(
        CommunityBenefitCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name="community_benefit_allocations_by_communty_benefit_category",
        verbose_name="Community Benefit Category",
    )
    trust_region = models.ForeignKey(
        TrustRegion,
        on_delete=models.SET_NULL,
        null=True,
        related_name="community_benefit_allocations_by_trust_region",
        verbose_name="Trust Region",
    )
    amount = models.DecimalField(
        "Amount (PGK)", max_digits=12, decimal_places=2, help_text="Amount in PNG kina."
    )
    year = models.PositiveIntegerField(
        "Year",
        null=True,
        validators=[MinValueValidator(1900), MaxValueValidator(datetime.now().year)],
    )

    def __str__(self):
        formatted_amount = "{:,.2f}".format(self.amount)
        return f"{self.community_benefit_category.name} - {formatted_amount} PGK - {self.trust_region.name}"

    class Meta:
        verbose_name = "Community Benefit Allocation"
        verbose_name_plural = "Community Benefit Allocations"
