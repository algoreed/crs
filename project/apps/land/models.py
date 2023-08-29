from django.db import models
from datetime import datetime
from apps.main.models import (
    Tribe,
    Clan,
    Province,
    District,
    LocalLevelGovernment,
    Company,
)


# Base model containing common fields
class BaseLand(models.Model):
    land_name = models.CharField("Land Name", max_length=255)
    province = models.ForeignKey(
        Province,
        on_delete=models.CASCADE,
        blank=True,
        related_name="%(app_label)s_%(class)s_related",
        verbose_name="Province",
    )
    district = models.ForeignKey(
        District,
        on_delete=models.CASCADE,
        blank=True,
        related_name="%(app_label)s_%(class)s_related",
        verbose_name="District",
    )
    llg = models.ForeignKey(
        LocalLevelGovernment,
        on_delete=models.CASCADE,
        blank=True,
        related_name="%(app_label)s_%(class)s_related",
        verbose_name="LLG",
    )
    description = models.TextField("Description", blank=True)

    images = models.FileField("Images", upload_to="lands/images/", blank=True)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True


# TODO link with people
class LandOwners(models.Model):
    name = models.CharField("Name", max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Land Owner"
        verbose_name_plural = "Land Owners"
        ordering = ["name"]


class BaseTenement(models.Model):
    title = models.CharField("Title", max_length=255)
    lease_holder = models.ForeignKey(
        Company,
        on_delete=models.CASCADE,
        blank=True,
        related_name="%(app_label)s_%(class)s_related",
        verbose_name="Lease Holder",
    )
    catalogueNumber = models.CharField("Catalogue Number", blank=True, max_length=50)
    volume = models.CharField(
        "Volume",
        max_length=50,
        blank=True,
    )
    folio = models.CharField(
        "Folio",
        max_length=50,
        blank=True,
    )
    fourmil = models.CharField(
        "Fourmil",
        max_length=50,
        blank=True,
    )
    milinch = models.CharField(
        "Milinch",
        max_length=50,
        blank=True,
    )
    portion = models.CharField(
        "Portion",
        max_length=50,
        blank=True,
    )

    class Meta:
        abstract = True


class LandTenement(BaseLand, BaseTenement):
    type_of_tenement = models.CharField(
        "Type of Tenement",
        blank=True,
        max_length=255,
        choices=[
            ("Freehold", "Freehold"),
            ("Leasehold", "Leasehold"),
            ("Customary", "Customary"),
            ("Commercial", "Commercial"),
            ("State or Public Land", "State or Public Land"),
        ],
    )

    @property
    def days_until_rental_due(self):
        if hasattr(
            self,
            "land_tenement_acquisition_by_land_tenement"
            and self.land_tenement_acquisition_by_land_tenement.rental_due_date,
        ):
            rental_due = (
                self.land_tenement_acquisition_by_land_tenement.rental_due_date
                - datetime.date(datetime.now())
            )
            return rental_due

        return None

    class Meta:
        verbose_name = "Land Tenement"
        verbose_name_plural = "Land Tenements"
        ordering = ["title"]


class LandTenementAcquisition(models.Model):
    land_tenement = models.OneToOneField(
        LandTenement,
        on_delete=models.SET_NULL,
        null=True,
        related_name="land_tenement_acquisition_by_land_tenement",
        verbose_name="Land Tenement",
    )
    acquisition_date = models.DateField("Acquisition Date", blank=True, null=True)
    start_date = models.DateField("Start Date", blank=True, null=True)
    end_date = models.DateField("End Date", blank=True, null=True)
    duration_years = models.IntegerField(
        "Duration (Term)",
        blank=True,
        null=True,
        help_text="Duration of the lease in years.",
    )
    purchase_price = models.DecimalField(
        "Purchace Price (PGK)",
        max_digits=15,
        decimal_places=2,
        blank=True,
        help_text="Purchase price in PNG kina",
    )
    rental_amount = models.DecimalField(
        "Rental Amount (PGK)",
        max_digits=15,
        decimal_places=2,
        blank=True,
        help_text="Rental amount in PNG kina",
    )
    rental_due_date = models.DateField("Rental Due Date", blank=True)
    notes = models.TextField("Notes", blank=True)

    def __str__(self):
        return f"{self.land_tenement} is acquired by {self.lease_holder.name}"

    class Meta:
        verbose_name = "Land Tenement Acquisition"
        verbose_name_plural = "Land Tenement Acquisitions"


class LandTenementRental(models.Model):
    land_tenement = models.ForeignKey(
        LandTenement,
        on_delete=models.SET_NULL,
        null=True,
        related_name="land_tenement_rentals_by_land_tenement",
        verbose_name="Land Tenement",
    )
    payment_date = models.DateField("Payment Date")
    amount_paid = models.DecimalField("Amount Paid", max_digits=15, decimal_places=2)
    payment_method = models.CharField(
        "Payment Method",
        blank=True,
        null=True,
        max_length=50,
        choices=[
            ("Bank Transfer", "Bank Transfer"),
            ("Cash", "Cash"),
            ("Cheque", "Cheque"),
            ("Online Payment", "Online Payment"),
        ],
    )
    receipt_number = models.CharField(
        "Receipt Number", max_length=50, blank=True, null=True
    )
    payer_details = models.TextField("Payer Details", blank=True, null=True)
    payment_status = models.CharField(
        "Payment Status",
        blank=True,
        null=True,
        max_length=20,
        choices=[
            ("Pending", "Pending"),
            ("Completed", "Completed"),
            ("Failed", "Failed"),
        ],
    )
    notes = models.TextField("Notes", blank=True, null=True)

    def __str__(self):
        return f"Payment for {self.land_tenement.title} on {self.payment_date}"

    class Meta:
        verbose_name = "Land Tenement Rental"
        verbose_name_plural = "Land Tenement Rentals"
        ordering = [
            "-payment_date",
        ]


class LandTenementSurvey(models.Model):
    land_tenement = models.ForeignKey(
        LandTenement,
        on_delete=models.SET_NULL,
        null=True,
        related_name="land_tenement_surveys_by_land_tenement",
        verbose_name="Land Tenement",
    )
    survey_date = models.DateField("Survey Date", blank=True)
    surveyor_name = models.CharField("Surveyor Name", max_length=255)

    class Meta:
        verbose_name = "Land Tenement Survey"
        verbose_name_plural = "Land Tenement Surveys"
        ordering = ["-survey_date"]


class LandTenementSurveyPoint(models.Model):
    land_tenement_survey = models.ForeignKey(
        LandTenementSurvey,
        on_delete=models.SET_NULL,
        null=True,
        related_name="land_tenemenet_survey_points_by_land_tenement_survey",
        verbose_name="Land Tenement Survey",
    )
    latitude = models.DecimalField(
        "Latitude", blank=True, max_digits=9, decimal_places=6
    )
    longitude = models.DecimalField(
        "Longitude", blank=True, max_digits=9, decimal_places=6
    )

    class Meta:
        verbose_name = "Land Tenement Survey Point"
        verbose_name_plural = "Land Tenement Survey Points"


class MiningTenement(BaseLand, BaseTenement):
    type_of_tenement = models.CharField(
        "Type of Tenement",
        blank=True,
        max_length=255,
        choices=[
            ("Special Mining Lease (SML)", "Special Mining Lease (SML)"),
            ("Lease for Mining Purpose (LMP)", "Lease for Mining Purpose (LMP)"),
            (
                "Lease Compensation Arrangement (LCA)",
                "Lease Compensation Arrangement (LCA)",
            ),
            ("Exploration Lease", "Exploration Lease"),
        ],
    )

    @property
    def days_until_rental_due(self):
        if hasattr(
            self,
            "mining_tenement_acquisition_by_mining_tenement"
            and self.mining_tenement_acquisition_by_mining_tenement.rental_due_date,
        ):
            rental_due = (
                self.mining_tenement_acquisition_by_mining_tenement.rental_due_date
                - datetime.date(datetime.now())
            )
            return rental_due
        return None

    class Meta:
        verbose_name = "Mining Tenement"
        verbose_name_plural = "Mining Tenements"
        ordering = ["title"]


class MiningTenementAcquisition(models.Model):
    mining_tenement = models.OneToOneField(
        MiningTenement,
        on_delete=models.SET_NULL,
        null=True,
        related_name="mining_tenement_acquisition_by_mining_tenement",
        verbose_name="Mining Tenement",
    )
    acquisition_date = models.DateField("Acquisition Date", blank=True, null=True)
    start_date = models.DateField("Start Date", blank=True, null=True)
    end_date = models.DateField("End Date", blank=True, null=True)
    duration_years = models.IntegerField(
        "Duration (Term)",
        blank=True,
        null=True,
        help_text="Duration of the lease in years.",
    )
    purchase_price = models.DecimalField(
        "Purchace Price (PGK)",
        max_digits=15,
        decimal_places=2,
        blank=True,
        help_text="Purchase price in PNG kina",
    )
    rental_amount = models.DecimalField(
        "Rental Amount (PGK)",
        max_digits=15,
        decimal_places=2,
        blank=True,
        help_text="Rental amount in PNG kina",
    )
    rental_due_date = models.DateField("Rental Due Date", blank=True)
    notes = models.TextField("Notes", blank=True)

    def __str__(self):
        return f"{self.land_tenement} is acquired by {self.lease_holder.name}"

    class Meta:
        verbose_name = "Mining Tenement Acquisition"
        verbose_name_plural = "Mining Tenement Acquisitions"


class MiningTenementRental(models.Model):
    mining_tenement = models.ForeignKey(
        MiningTenement,
        on_delete=models.SET_NULL,
        null=True,
        related_name="mining_tenement_rentals_by_mining_tenement",
        verbose_name="Mining Tenement",
    )
    payment_date = models.DateField("Payment Date")
    amount_paid = models.DecimalField("Amount Paid", max_digits=15, decimal_places=2)
    payment_method = models.CharField(
        "Payment Method",
        blank=True,
        null=True,
        max_length=50,
        choices=[
            ("Bank Transfer", "Bank Transfer"),
            ("Cash", "Cash"),
            ("Cheque", "Cheque"),
            ("Online Payment", "Online Payment"),
        ],
    )
    receipt_number = models.CharField(
        "Receipt Number", max_length=50, blank=True, null=True
    )
    payer_details = models.TextField("Payer Details", blank=True, null=True)
    payment_status = models.CharField(
        "Payment Status",
        blank=True,
        null=True,
        max_length=20,
        choices=[
            ("Pending", "Pending"),
            ("Completed", "Completed"),
            ("Failed", "Failed"),
        ],
    )
    notes = models.TextField("Notes", blank=True, null=True)

    def __str__(self):
        return f"Payment for {self.land_tenement.title} on {self.payment_date}"

    class Meta:
        verbose_name = "Mining Tenement Rental"
        verbose_name_plural = "Mining Tenement Rentals"
        ordering = [
            "-payment_date",
        ]


class MiningTenementSurvey(models.Model):
    mininig_tenement = models.ForeignKey(
        MiningTenement,
        on_delete=models.SET_NULL,
        null=True,
        related_name="mining_tenement_surveys_by_mining_tenement",
        verbose_name="Mining Tenement",
    )
    survey_date = models.DateField("Survey Date", blank=True)
    surveyor_name = models.CharField("Surveyor Name", max_length=255)

    class Meta:
        verbose_name = "Mining Tenement Survey"
        verbose_name_plural = "Mining Tenement Surveys"
        ordering = ["-survey_date"]


class MiningTenementSurveyPoint(models.Model):
    mining_tenement_survey = models.ForeignKey(
        MiningTenementSurvey,
        on_delete=models.SET_NULL,
        null=True,
        related_name="mining_tenemenet_survey_points_by_mining_tenement_survey",
        verbose_name="Mining Tenement Survey",
    )
    latitude = models.DecimalField(
        "Latitude", blank=True, max_digits=9, decimal_places=6
    )
    longitude = models.DecimalField(
        "Longitude", blank=True, max_digits=9, decimal_places=6
    )

    class Meta:
        verbose_name = "Mining Tenement Survey Point"
        verbose_name_plural = "Mining Tenement Survey Points"
