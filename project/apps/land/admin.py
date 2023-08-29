from django.contrib import admin
from django.contrib.admin.sites import site as default_site
from apps.main.admin import custom_admin_site
from .models import (
    LandOwners,
    LandTenement,
    LandTenementAcquisition,
    LandTenementRental,
    LandTenementSurvey,
    LandTenementSurveyPoint,
    MiningTenement,
    MiningTenementAcquisition,
    MiningTenementRental,
    MiningTenementSurvey,
    MiningTenementSurveyPoint,
)

# Register your models here.


@admin.register(LandOwners)
class LandOwnersAdmin(admin.ModelAdmin):
    list_display = ["name"]
    search_fields = ["name"]
    list_per_page = 50
    ordering = ["name"]


@admin.register(LandTenement)
class LandTenementAdmin(admin.ModelAdmin):
    list_display = [
        "land_name",
        "title",
        "province",
        "district",
        "llg",
        "type_of_tenement",
        "days_until_rental_due_alert",
    ]
    search_fields = ["land_name", "type_of_tenement"]
    list_filter = ["type_of_tenement", "province", "district", "llg"]
    list_per_page = 50
    ordering = ["title"]
    fieldsets = (
        (
            "Basic Info",
            {"fields": ("land_name", "description", "images", "type_of_tenement")},
        ),
        ("Location", {"fields": ("province", "district", "llg")}),
        (
            "Tenement Details",
            {
                "fields": (
                    "title",
                    "lease_holder",
                    "catalogueNumber",
                    "volume",
                    "folio",
                    "fourmil",
                    "milinch",
                    "portion",
                )
            },
        ),
    )

    def days_until_rental_due_alert(self, obj):
        days = obj.days_until_rental_due
        if days is not None:
            if days < 0:
                return f"Overdue by {-days} days"
            elif days == 0:
                return "Due today"
            else:
                return f"Due in {days} days"
        return "No due date set"

    days_until_rental_due_alert.short_description = "Rental Due Alert"


@admin.register(LandTenementAcquisition)
class LandTenementAcquisitionAdmin(admin.ModelAdmin):
    list_display = [
        "land_tenement",
        "purchase_price",
        "rental_amount",
        "rental_due_date",
    ]
    search_fields = ["land_tenement__land_name"]
    list_filter = ["land_tenement__type_of_tenement"]
    list_per_page = 50
    ordering = ["land_tenement"]
    fieldsets = (
        ("Land Tenement Info", {"fields": ("land_tenement",)}),
        (
            "Acquisition Details",
            {
                "fields": (
                    "acquisition_date",
                    "duration_years",
                    "start_date",
                    "end_date",
                    "purchase_price",
                    "rental_amount",
                    "rental_due_date",
                    "notes",
                )
            },
        ),
    )


@admin.register(LandTenementRental)
class LandTenementRentalAdmin(admin.ModelAdmin):
    list_display = ["land_tenement", "payment_date", "amount_paid", "payment_method"]
    search_fields = ["land_tenement__land_name"]
    list_filter = ["payment_method", "payment_status"]
    list_per_page = 50
    ordering = ["-payment_date"]
    fieldsets = (
        ("Land Tenement Info", {"fields": ("land_tenement",)}),
        (
            "Payment Details",
            {
                "fields": (
                    "payment_date",
                    "amount_paid",
                    "payment_method",
                    "receipt_number",
                    "payer_details",
                    "payment_status",
                    "notes",
                )
            },
        ),
    )


@admin.register(LandTenementSurvey)
class LandTenementSurveyAdmin(admin.ModelAdmin):
    list_display = ["land_tenement", "survey_date", "surveyor_name"]
    search_fields = ["land_tenement__land_name", "surveyor_name"]
    list_filter = ["survey_date"]
    list_per_page = 50
    ordering = ["-survey_date"]
    fieldsets = (
        ("Land Tenement Info", {"fields": ("land_tenement",)}),
        ("Survey Details", {"fields": ("survey_date", "surveyor_name")}),
    )


@admin.register(LandTenementSurveyPoint)
class LandTenementSurveyPointAdmin(admin.ModelAdmin):
    list_display = ["land_tenement_survey", "latitude", "longitude"]
    search_fields = ["land_tenement_survey__land_tenement__land_name"]
    list_per_page = 50
    ordering = ["land_tenement_survey"]
    fieldsets = (
        ("Land Tenement Survey Info", {"fields": ("land_tenement_survey",)}),
        ("Point Details", {"fields": ("latitude", "longitude")}),
    )


@admin.register(MiningTenement)
class MiningTenementAdmin(admin.ModelAdmin):
    list_display = [
        "land_name",
        "title",
        "province",
        "district",
        "llg",
        "type_of_tenement",
        "days_until_rental_due_alert",
    ]
    search_fields = ["land_name", "type_of_tenement"]
    list_filter = ["type_of_tenement", "province", "district", "llg"]
    list_per_page = 50
    ordering = ["title"]
    fieldsets = (
        (
            "Basic Info",
            {"fields": ("land_name", "description", "images", "type_of_tenement")},
        ),
        ("Location", {"fields": ("province", "district", "llg")}),
        (
            "Tenement Details",
            {
                "fields": (
                    "title",
                    "lease_holder",
                    "catalogueNumber",
                    "volume",
                    "folio",
                    "fourmil",
                    "milinch",
                    "portion",
                )
            },
        ),
    )

    def days_until_rental_due_alert(self, obj):
        days = obj.days_until_rental_due
        if days is not None:
            if days < 0:
                return f"Overdue by {-days} days"
            elif days == 0:
                return "Due today"
            else:
                return f"Due in {days} days"
        return "No due date set"

    days_until_rental_due_alert.short_description = "Rental Due Alert"


@admin.register(MiningTenementAcquisition)
class MiningTenementAcquisitionAdmin(admin.ModelAdmin):
    list_display = [
        "mining_tenement",
        "purchase_price",
        "rental_amount",
        "rental_due_date",
    ]
    search_fields = ["mining_tenement__land_name"]
    list_filter = ["mining_tenement__type_of_tenement"]
    list_per_page = 50
    ordering = ["mining_tenement"]
    fieldsets = (
        ("Mining Tenement Info", {"fields": ("mining_tenement",)}),
        (
            "Acquisition Details",
            {
                "fields": (
                    "acquisition_date",
                    "duration_years",
                    "start_date",
                    "end_date",
                    "purchase_price",
                    "rental_amount",
                    "rental_due_date",
                    "notes",
                )
            },
        ),
    )


@admin.register(MiningTenementRental)
class MiningTenementRentalAdmin(admin.ModelAdmin):
    list_display = ["mining_tenement", "payment_date", "amount_paid", "payment_method"]
    search_fields = ["mining_tenement__land_name"]
    list_filter = ["payment_method", "payment_status"]
    list_per_page = 50
    ordering = ["-payment_date"]
    fieldsets = (
        ("Mining Tenement Info", {"fields": ("mining_tenement",)}),
        (
            "Payment Details",
            {
                "fields": (
                    "payment_date",
                    "amount_paid",
                    "payment_method",
                    "receipt_number",
                    "payer_details",
                    "payment_status",
                    "notes",
                )
            },
        ),
    )


@admin.register(MiningTenementSurvey)
class MiningTenementSurveyAdmin(admin.ModelAdmin):
    list_display = ["mininig_tenement", "survey_date", "surveyor_name"]
    search_fields = ["mininig_tenement__land_name", "surveyor_name"]
    list_filter = ["survey_date"]
    list_per_page = 50
    ordering = ["-survey_date"]
    fieldsets = (
        ("Mining Tenement Info", {"fields": ("mininig_tenement",)}),
        ("Survey Details", {"fields": ("survey_date", "surveyor_name")}),
    )


@admin.register(MiningTenementSurveyPoint)
class MiningTenementSurveyPointAdmin(admin.ModelAdmin):
    list_display = ["mining_tenement_survey", "latitude", "longitude"]
    search_fields = ["mining_tenement_survey__mininig_tenement__land_name"]
    list_per_page = 50
    ordering = ["mining_tenement_survey"]
    fieldsets = (
        ("Mining Tenement Survey Info", {"fields": ("mining_tenement_survey",)}),
        ("Point Details", {"fields": ("latitude", "longitude")}),
    )


for model, model_admin in default_site._registry.items():
    if model not in custom_admin_site._registry:
        custom_admin_site.register(model, type(model_admin))
