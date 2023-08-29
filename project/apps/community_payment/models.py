from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from datetime import datetime, date
from apps.main.models import TrustRegion, TrustVillage, Bank
from apps.community_benefit.models import (
    CommunityBenefitCategory,
    CommunityBenefitAllocation,
)
from apps.community_context.models import Household

# Create your models here.


class AllocationDistribution(models.Model):
    trust_region = models.ForeignKey(
        TrustRegion,
        on_delete=models.SET_NULL,
        null=True,
        related_name="allocation_distributions_by_trust_region",
        verbose_name="Trust Region",
    )
    trust_village = models.ForeignKey(
        TrustVillage,
        on_delete=models.SET_NULL,
        null=True,
        related_name="allocation_distributions_by_trust_village",
        verbose_name="Trust Village",
    )
    benefit_category = models.ForeignKey(
        CommunityBenefitCategory,
        on_delete=models.SET_NULL,
        null=True,
        related_name="allocation_distributions_by_benefit_category",
        verbose_name="Benefit Category",
    )
    benefit_allocation = models.ForeignKey(
        CommunityBenefitAllocation,
        on_delete=models.SET_NULL,
        null=True,
        related_name="allocation_distributions_by_benefit_allocation",
        verbose_name="Benefit Allocation",
    )
    # amount

    class Meta:
        verbose_name = "Allocation Distribution"
        verbose_name_plural = "Allocation Distributions"
