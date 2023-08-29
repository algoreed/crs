from django.contrib import admin
from django.db.models import F
from django.db import models
from django.db.models import Case, When, Value, IntegerField
from django.contrib.admin.sites import site as default_site
from apps.main.admin import custom_admin_site
from dal_select2.widgets import ModelSelect2
from .models import Dwelling, Household, CommunityPerson, HouseholdBankAccount


# Register your models here.


@admin.register(Dwelling)
class DwellingAdmin(admin.ModelAdmin):
    list_display = (
        "trust_region",
        "trust_village",
        "dwelling_number",
        "dwelling_type",
        "construction_year",
    )
    search_fields = (
        "trust_region__name",
        "trust_village__name",
        "dwelling_number",
    )
    list_filter = (
        "trust_region",
        "trust_village",
        "dwelling_type",
    )
    list_per_page = 50
    ordering = (
        "trust_region",
        "trust_village",
        "dwelling_number",
    )


class HeadOfHouseholdInline(
    admin.StackedInline
):  # Using StackedInline for a vertical display
    model = CommunityPerson
    verbose_name = "Head of Household"
    verbose_name_plural = "Head of Household"
    extra = 0
    max_num = 1
    fields = (
        "first_name",
        "last_name",
        "sex",
        "relationship_to_head",
        "age_group",
        "date_of_birth",
        "trust_region",
        "trust_village",
        "dwelling_number",
        "household_number",
        "occupation",
        "education_level",
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.filter(id=F("household_by_head_of_household"))

    def has_add_permission(self, request, obj=None):
        # Ensure only one head of household can be added
        if obj and obj.head_of_household:
            return False
        return super().has_add_permission(request, obj)


class MembersInline(admin.StackedInline):
    model = CommunityPerson
    verbose_name = "Member"
    verbose_name_plural = "Members"
    extra = 0
    fields = (
        "first_name",
        "last_name",
        "sex",
        "relationship_to_head",
        "age_group",
        "date_of_birth",
        "trust_region",
        "trust_village",
        "dwelling_number",
        "household_number",
        "occupation",
        "education_level",
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)

        # Exclude the head of the household
        qs = qs.exclude(id=F("household_by_head_of_household__head_of_household"))

        # Order so that the head (if any) comes first, followed by others ordered by first_name and last_name
        qs = qs.annotate(
            is_head=Case(
                When(relationship_to_head="Head", then=Value(1)),
                default=Value(0),
                output_field=models.IntegerField(),
            )
        ).order_by("-is_head", "first_name", "last_name")

        return qs


class HouseholdBankAccountInline(admin.StackedInline):
    model = HouseholdBankAccount
    extra = 0
    max_num = 1  # Restrict to only one bank account per household
    verbose_name = "Household Bank Account"
    verbose_name_plural = "Household Bank Accounts"

    #  Ensure only one bank account is added per household
    def has_add_permission(self, request, obj=None):
        if obj and obj.householdbankaccount_set.exists():
            return False
        return super().has_add_permission(request, obj)


@admin.register(Household)
class HouseholdAdmin(admin.ModelAdmin):
    inlines = [HouseholdBankAccountInline, HeadOfHouseholdInline, MembersInline]

    list_display = (
        "trust_region",
        "trust_village",
        "dwelling_number_display",
        "household_number",
        "head_of_household_name",
    )
    search_fields = (
        "head_of_household__first_name",
        "trust_village__name",
        "trust_region__name",
    )
    list_filter = (
        "trust_region",
        "trust_village",
        "dwelling_number",
    )
    list_per_page = 50
    ordering = ("dwelling_number",)

    fieldsets = (
        (
            "Basic Info",
            {
                "fields": (
                    "trust_region",
                    "trust_village",
                    "dwelling_number",
                    "household_number",
                    "primary_income_source",
                )
            },
        ),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "dwelling_number":
            kwargs["widget"] = ModelSelect2(url="dwelling_autocomplete")
            return super().formfield_for_foreignkey(db_field, request, **kwargs)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def trust_village_name(self, obj):
        return obj.trust_village.name if obj.trust_village else None

    trust_village_name.short_description = "Trust Village Name"

    def dwelling_number_display(self, obj):
        return obj.dwelling_number.dwelling_number if obj.dwelling_number else None

    dwelling_number_display.short_description = "Dwelling Number"

    def head_of_household_name(self, obj):
        if obj.head_of_household:
            return (
                f"{obj.head_of_household.first_name} {obj.head_of_household.last_name}"
            )
        return None

    head_of_household_name.short_description = "Head of Household"


@admin.register(CommunityPerson)
class CommunityPersonAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "sex",
        "relationship_to_head",
        "age_group",
        "date_of_birth",
        "trust_region",
        "trust_village",
        "dwelling_number",
        "household_number",
        "occupation",
        "education_level",
    )
    search_fields = (
        "first_name",
        "last_name",
        "trust_region__name",
        "trust_village__name",
        "dwelling_number__dwelling_number",
        "household_number__household_number",
    )
    list_filter = (
        "sex",
        "relationship_to_head",
        "age_group",
        "trust_region",
        "trust_village",
        "occupation",
        "education_level",
    )
    list_per_page = 50
    ordering = (
        "trust_region",
        "trust_village",
        "last_name",
        "first_name",
    )

    fieldsets = (
        (
            None,
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "sex",
                    "relationship_to_head",
                    "age_group",
                    "date_of_birth",
                    "trust_region",
                    "trust_village",
                    "dwelling_number",
                    "household_number",
                    "occupation",
                    "education_level",
                )
            },
        ),
    )

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.annotate(
            is_head=Case(
                When(relationship_to_head="Head", then=Value(1)),
                default=Value(0),
                output_field=IntegerField(),
            )
        ).order_by("-is_head", "first_name", "last_name")


@admin.register(HouseholdBankAccount)
class HouseholdBankAccountAdmin(admin.ModelAdmin):
    list_display = (
        "account_name",
        "account_number",
        "bank_initials",
        "branch",
        "status",
        "household",
    )
    search_fields = (
        "account_name",
        "account_number",
        "branch",
        "status",
        "household__first_name",
        "household__last_name",
    )
    list_filter = ("bank_initials", "status", "household")
    list_per_page = 50
    ordering = (
        "account_name",
        "status",
    )

    fieldsets = (
        (
            "Bank Account Details",
            {
                "fields": (
                    "account_name",
                    "account_number",
                    "bank_initials",
                    "branch",
                    "status",
                )
            },
        ),
        (
            "Household Details",
            {
                "fields": ("household",),
            },
        ),
    )


for model, model_admin in default_site._registry.items():
    if model not in custom_admin_site._registry:
        custom_admin_site.register(model, type(model_admin))
