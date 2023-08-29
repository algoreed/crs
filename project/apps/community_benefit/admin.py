from django.contrib import admin
from django.contrib.admin.sites import site as default_site
from apps.main.admin import custom_admin_site
from .models import CommunityBenefitCategory, CommunityBenefitAllocation

# Register your models here.


@admin.register(CommunityBenefitCategory)
class CommunityBenefitCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "trust_region", "year")
    search_fields = ("name", "trust_region__name", "year")
    list_filter = ("name", "trust_region", "year")
    list_per_page = 25
    ordering = ("name",)

    fieldsets = (
        (None, {"fields": ("name", "trust_region", "year")}),
        # Add any additional fieldsets as needed
        # ('Advanced options', {
        #     'classes': ('collapse',),
        #     'fields': ('...'),
        # }),
    )


@admin.register(CommunityBenefitAllocation)
class CommunityBenefitAllocationAdmin(admin.ModelAdmin):
    list_display = (
        "community_benefit_category",
        "trust_region",
        "formatted_amount",
        "year",
    )
    search_fields = (
        "community_benefit_category__name",
        "trust_region__name",
        "year",
        "amount",
    )
    list_filter = ("community_benefit_category", "trust_region", "year")
    list_per_page = 25
    ordering = ("-year", "community_benefit_category")

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "community_benefit_category",
                    "trust_region",
                    "amount",
                    "year",
                )
            },
        ),
    )

    def formatted_amount(self, obj):
        return "{:,.2f}".format(obj.amount)

    formatted_amount.short_description = "Amount (PGK)"


for model, model_admin in default_site._registry.items():
    if model not in custom_admin_site._registry:
        custom_admin_site.register(model, type(model_admin))
