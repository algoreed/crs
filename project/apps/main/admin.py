from django.contrib import admin
from django.contrib.admin.sites import site as default_site
from django.contrib.admin import AdminSite
from .models import (
    Country,
    Organization,
    Company,
    Province,
    District,
    LocalLevelGovernment,
    TrustRegion,
    Village,
    TrustVillage,
    Tribe,
    Clan,
    Bank,
)


class CustomAdminSite(AdminSite):
    site_header = "CRS"
    site_title = "CRS"
    index_title = "Welcome to CRS"


custom_admin_site = CustomAdminSite(name="crs")


# Register your models here.


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
    list_filter = ["name"]
    list_per_page = 50
    ordering = ["name"]


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ["name", "email", "phone", "address"]
    search_fields = ["name", "email", "phone", "address"]
    list_filter = ["name"]
    list_per_page = 50
    ordering = ["name"]
    fieldsets = (
        (
            "Basic Info",
            {
                "fields": ("name",),
            },
        ),
        (
            "Contact Details",
            {
                "fields": ("email", "phone", "address"),
            },
        ),
    )


@admin.register(Company)
class CompanyAdmin(OrganizationAdmin):
    # Inherits from OrganizationAdmin for similar fields and configurations
    pass


@admin.register(Province)
class ProvinceAdmin(admin.ModelAdmin):
    list_display = ["name", "country"]
    search_fields = ["name"]
    list_filter = ["name", "country"]
    list_per_page = 50
    ordering = ["name"]
    fieldsets = (
        (
            "Province Details",
            {
                "fields": (
                    "name",
                    "country",
                ),
            },
        ),
    )


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ["name", "province"]
    search_fields = ["name"]
    list_filter = ["name", "province"]
    list_per_page = 50
    ordering = ["name"]
    fieldsets = (
        (
            "District Details",
            {
                "fields": (
                    "name",
                    "province",
                ),
            },
        ),
    )


@admin.register(LocalLevelGovernment)
class LLGAdmin(admin.ModelAdmin):
    list_display = ["name", "display_province", "display_district"]
    search_fields = ["name"]
    list_filter = ["name", "province", "district"]
    list_per_page = 50
    ordering = ["name"]
    fieldsets = (
        (
            "LLG Details",
            {
                "fields": (
                    "name",
                    "province",
                    "district",
                ),
            },
        ),
    )

    def display_province(self, obj):
        return obj.province.name if obj.province else "-"

    display_province.short_description = "Province"

    def display_district(self, obj):
        return obj.district.name if obj.district else "-"

    display_district.short_description = "District"


@admin.register(TrustRegion)
class TrustRegionAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
    list_filter = [
        "name",
    ]
    list_per_page = 50
    ordering = ["name"]
    fieldsets = (
        (
            "Trust Region Details",
            {
                "fields": ("name",),
            },
        ),
    )


@admin.register(Village)
class VillageAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "display_province",
        "display_district",
        "llg",
    ]
    search_fields = ["name"]
    list_filter = [
        "name",
        "province",
        "district",
        "llg",
    ]
    list_per_page = 50
    ordering = ["name"]
    fieldsets = (
        (
            "Village Details",
            {
                "fields": (
                    "name",
                    "province",
                    "district",
                    "llg",
                ),
            },
        ),
    )

    def display_province(self, obj):
        return obj.province.name if obj.province else "-"

    display_province.short_description = "Province"

    def display_district(self, obj):
        return obj.district.name if obj.district else "-"

    display_district.short_description = "District"


@admin.register(TrustVillage)
class TrustVillageAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "display_province",
        "display_district",
        "llg",
        "display_trust_region",
    ]
    search_fields = ["name"]
    list_filter = ["name", "province", "district", "llg", "trust_region"]
    list_per_page = 50
    ordering = ["name"]
    fieldsets = (
        (
            "Village Details",
            {
                "fields": (
                    "name",
                    "province",
                    "district",
                    "llg",
                    "trust_region",
                ),
            },
        ),
    )

    def display_province(self, obj):
        return obj.province.name if obj.province else "-"

    display_province.short_description = "Province"

    def display_district(self, obj):
        return obj.district.name if obj.district else "-"

    display_district.short_description = "District"

    def display_trust_region(self, obj):
        return obj.trust_region.name if obj.trust_region else "-"

    display_trust_region.short_description = "Trust Region"


@admin.register(Tribe)
class TribeAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "display_province",
    ]
    search_fields = ["name"]
    list_filter = [
        "name",
        "province",
    ]
    list_per_page = 50
    ordering = ["name"]
    fieldsets = (
        (
            "Clan Details",
            {
                "fields": (
                    "name",
                    "province",
                ),
            },
        ),
    )

    def display_province(self, obj):
        return obj.province.name if obj.province else "-"


@admin.register(Clan)
class ClanAdmin(admin.ModelAdmin):
    list_display = [
        "name",
        "display_province",
        "display_district",
        "llg",
        "display_village",
        "display_trust_village",
        "tribe",
    ]
    search_fields = ["name"]
    list_filter = ["name", "province", "village", "trust_village", "tribe"]
    list_per_page = 50
    ordering = ["name"]
    fieldsets = (
        (
            "Clan Details",
            {
                "fields": (
                    "name",
                    "province",
                    "district",
                    "llg",
                    "village",
                    "trust_village",
                    "tribe",
                ),
            },
        ),
    )

    def display_province(self, obj):
        return obj.province.name if obj.province else "-"

    display_province.short_description = "Province"

    def display_district(self, obj):
        return obj.district.name if obj.district else "-"

    display_district.short_description = "District"

    def display_village(self, obj):
        # Return a string representation of the ManyToManyField
        return ", ".join([str(item) for item in obj.village.all()])

    display_village.short_description = "Village"

    def display_trust_village(self, obj):
        # Return a string representation of the ManyToManyField
        return ", ".join([str(item) for item in obj.trust_village.all()])

    display_trust_village.short_description = "Trust Village"


@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ("bank_name", "bank_initials", "account_number_length")
    search_fields = ("bank_name", "bank_initials")
    list_filter = ("bank_name",)
    list_per_page = 10
    ordering = (
        "bank_name",
        "bank_initials",
    )  # Alphabetical order by bank name and initials

    fieldsets = (
        (
            "Bank Information",
            {"fields": ("bank_name", "bank_initials", "account_number_length")},
        ),
    )


for model, model_admin in default_site._registry.items():
    if model not in custom_admin_site._registry:
        custom_admin_site.register(model, type(model_admin))
