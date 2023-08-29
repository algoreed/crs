from django.db import models

# Create your models here.


class NamedEntity(models.Model):
    name = models.CharField("Name", max_length=255, unique=True)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Country(NamedEntity):
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Country"
        verbose_name_plural = "Countries"
        ordering = ["name"]


class Organization(NamedEntity):
    address = models.TextField("Address", blank=True, null=True)
    phone = models.CharField("Phone", blank=True, null=True, max_length=25)
    email = models.EmailField("Email", blank=True, null=True, max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Organization"
        verbose_name_plural = "Organizations"
        ordering = ["name"]


class Company(NamedEntity):
    phone = models.CharField("Phone", blank=True, null=True, max_length=25)
    email = models.EmailField("Email", blank=True, null=True, max_length=255)
    address = models.TextField("Address", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Company"
        verbose_name_plural = "Companies"
        ordering = ["name"]


class Province(NamedEntity):
    country = models.ForeignKey(
        Country,
        on_delete=models.SET_NULL,
        null=True,
        related_name="provinces_by_country",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Province"
        verbose_name_plural = "Provinces"
        ordering = ["name"]


class District(NamedEntity):
    province = models.ForeignKey(
        Province,
        on_delete=models.SET_NULL,
        null=True,
        related_name="districts_by_province",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "District"
        verbose_name_plural = "Districts"
        ordering = ["name"]


class LocalLevelGovernment(NamedEntity):
    province = models.ForeignKey(
        Province, on_delete=models.SET_NULL, null=True, related_name="llgs_by_province"
    )
    district = models.ForeignKey(
        District, on_delete=models.SET_NULL, null=True, related_name="llgs_by_districts"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "LLG"
        verbose_name_plural = "LLGs"
        ordering = ["name"]


class TrustRegion(NamedEntity):
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Trust Region"
        verbose_name_plural = "Trust Regions"
        ordering = ["name"]


class BaseVillage(NamedEntity):
    province = models.ForeignKey(
        Province,
        on_delete=models.SET_NULL,
        null=True,
        related_name="villages_by_province",
        verbose_name="Province",
    )
    district = models.ForeignKey(
        District,
        on_delete=models.SET_NULL,
        null=True,
        related_name="villages_by_district",
        verbose_name="District",
    )
    llg = models.ForeignKey(
        LocalLevelGovernment,
        on_delete=models.CASCADE,
        null=True,
        related_name="villages_by_llg",
        verbose_name="LLG",
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Village(BaseVillage):
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Villages"
        ordering = ["name"]


class TrustVillage(BaseVillage):
    province = models.ForeignKey(
        Province,
        on_delete=models.SET_NULL,
        null=True,
        related_name="trustvillage_by_province",  # Distinct related_name for TrustVillage
        verbose_name="Province",
    )
    district = models.ForeignKey(
        District,
        on_delete=models.SET_NULL,
        null=True,
        related_name="trustvillage_by_district",  # Distinct related_name for TrustVillage
        verbose_name="District",
    )
    llg = models.ForeignKey(
        LocalLevelGovernment,
        on_delete=models.CASCADE,
        null=True,
        related_name="trustvillage_by_llg",  # Distinct related_name for TrustVillage
        verbose_name="LLG",
    )
    trust_region = models.ForeignKey(
        TrustRegion,
        on_delete=models.SET_NULL,
        null=True,
        related_name="trust_villages_by_region",
        verbose_name="Trust Region",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Trust Village"
        verbose_name_plural = "Trust Villages"
        ordering = ["name"]


class Tribe(NamedEntity):
    province = models.ForeignKey(
        Province,
        on_delete=models.SET_NULL,
        null=True,
        related_name="tribes_by_province",
        verbose_name="Province",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Tribe"
        verbose_name_plural = "Tribes"
        ordering = ["name"]


class Clan(NamedEntity):
    province = models.ForeignKey(
        Province,
        on_delete=models.SET_NULL,
        null=True,
        related_name="clans_by_province",
        verbose_name="Province",
    )
    district = models.ForeignKey(
        District,
        on_delete=models.SET_NULL,
        null=True,
        related_name="clans_by_district",
        verbose_name="District",
    )
    llg = models.ForeignKey(
        LocalLevelGovernment,
        on_delete=models.SET_NULL,
        null=True,
        related_name="clans_by_llg",  # Distinct related_name for TrustVillage
        verbose_name="LLG",
    )
    tribe = models.ForeignKey(
        Tribe,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="clans_by_tribe",
        verbose_name="Tribe",
    )
    village = models.ManyToManyField(
        Village, blank=True, related_name="clans_by_village"
    )
    trust_village = models.ManyToManyField(
        TrustVillage, blank=True, related_name="clans_by_trust_village"
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Clan"
        verbose_name_plural = "Clans"
        ordering = ["name"]


class Bank(models.Model):
    bank_name = models.CharField(
        "Bank Name",
        max_length=255,
        choices=[
            ("Bank of South Pacific", "Bank of South Pacific"),
            ("Westpac Bank", "Westpac Bank"),
            ("Australia and New Zealand Bank", "Australia and New Zealand Bank"),
            ("Kina Bank", "Kina Bank"),
            ("Nil", "Nil"),
        ],
    )
    bank_initials = models.CharField(
        "Bank initials",
        max_length=3,
        choices=[
            ("BSP", "BSP"),
            ("WPC", "WPC"),
            ("ANZ", "ANZ"),
            ("KB", "KB"),
            ("Nil", "Nil"),
        ],
    )
    account_number_length = models.PositiveIntegerField("Account Number Length")

    def __str__(self):
        return self.bank_initials

    class Meta:
        verbose_name = "Bank"
        verbose_name_plural = "Banks"
