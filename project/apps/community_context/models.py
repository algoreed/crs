from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError
from datetime import datetime, date
from apps.main.models import TrustRegion, TrustVillage, Bank

# Create your models here.


class BasePerson(models.Model):
    first_name = models.CharField(
        "First Name",
        max_length=255,
    )
    last_name = models.CharField(
        "Last Name",
        max_length=255,
    )
    sex = models.CharField(
        "Sex",
        max_length=1,
        choices=[
            ("M", "Male"),
            ("F", "Female"),
        ],
    )

    class Meta:
        abstract = True


class CommunityPerson(BasePerson):
    sex = models.CharField(
        "Sex",
        max_length=1,
        choices=[
            ("M", "Male"),
            ("F", "Female"),
        ],
    )
    relationship_to_head = models.CharField(
        "Relationship to Head",
        max_length=255,
        choices=[
            ("Head", "Head"),
            ("Wife", "Wife"),
            ("Husband", "Husband"),
            ("Son", "Son"),
            ("Daughter", "Daughter"),
            ("Grandchild", "Grandchild"),
            ("Parent", "Parent"),
            ("Parent In-Law", "Parent In-Law"),
            ("Daughter In-Law", "Daughter In-Law"),
            ("Son In-Law", "Son In-Law"),
            ("Sister In-Law", "Sister In-Law"),
            ("Brother In-Law", "Brother In-Law"),
            ("Brother", "Brother"),
            ("Sister", "Sister"),
            ("Uncle", "Uncle"),
            ("Aunt", "Aunt"),
            ("Niece", "Niece"),
            ("Nephew", "Nephew"),
            ("Cousin", "Cousin"),
            ("Grandparent", "Grandparent"),
            ("Adopted child", "Adopted child"),
            ("Non relative", "Non relative"),
        ],
    )
    age_group = models.CharField(
        "Age Group",
        max_length=255,
        choices=[
            ("Baby", "Baby (0-2 years)"),
            ("Child", "Child (3-12 years)"),
            ("Teenage", "Teenage (13-19 years)"),
            ("Young Adult", "Young Adult (20-34)"),
            ("Middle-aged Adult", "Middle-aged Adult (35-64)"),
            (
                "Old Age",
                "Old Age (65-74 years young-old, 75-84 years middle-old, 85+ years very old)",
            ),
        ],
    )
    trust_region = models.ForeignKey(
        TrustRegion,
        on_delete=models.SET_NULL,
        null=True,
        related_name="community_persons_by_trust_region",
        verbose_name="Trust Region",
    )
    trust_village = models.ForeignKey(
        TrustVillage,
        on_delete=models.SET_NULL,
        null=True,
        related_name="community_persons_by_trust_village",
        verbose_name="Trust Village",
    )
    date_of_birth = models.DateField(
        "Date of Birth",
        blank=True,
        null=True,
        validators=[
            MinValueValidator(date(1900, 1, 1)),
            MaxValueValidator(date.today()),
        ],
    )
    dwelling_number = models.ForeignKey(
        "Dwelling",
        on_delete=models.SET_NULL,
        null=True,
        related_name="community_persons_by_dwelling_number",
        verbose_name="Dwelling Number",
    )
    household_number = models.ForeignKey(
        "Household",
        on_delete=models.SET_NULL,
        null=True,
        related_name="community_persons_by_household_number",
        verbose_name="Household Number",
    )
    occupation = models.CharField(
        "Occupation",
        blank=True,
        max_length=255,
        choices=[
            ("Farmer", "Farmer"),
            ("Fisherman", "Fisherman"),
            ("Teacher", "Teacher"),
            ("Doctor", "Doctor"),
            ("Nurse", "Nurse"),
            ("Engineer", "Engineer"),
            ("Clerk", "Clerk"),
            ("Salesperson", "Salesperson"),
            ("Miner", "Miner"),
            ("Driver", "Driver"),
            ("Cook", "Cook/Chef"),
            ("Service Worker", "Service Worker"),
            ("Cleaning Staff", "Cleaning Staff"),
            ("Security Guard", "Security Guard"),
            ("Office Worker", "Office Worker"),
            ("Student", "Student"),
            ("Retired", "Retired"),
            ("Homemaker", "Homemaker"),
            ("Artist", "Artist"),
            ("Musician", "Musician"),
            ("Actor", "Actor/Actress"),
            ("Writer", "Writer"),
            ("Politician", "Politician"),
            ("Lawyer", "Lawyer"),
            ("Unemployed", "Unemployed"),
            ("Other", "Other"),
        ],
    )
    education_level = models.CharField(
        "Education Level",
        blank=True,
        max_length=255,
        choices=[
            ("None", "No Formal Education"),
            ("Infant", "Infant/Not Yet in School"),
            ("Preschool", "Preschool"),
            ("Kindergarten", "Kindergarten"),
            ("Elementary Education", "Elementary Education"),
            ("Primary Education", "Primary Education"),
            ("Secondary Education", "Secondary Education"),
            ("Vocational/Trade School", "Vocational/Trade School"),
            ("Associate Degree", "Associate Degree"),
            ("Bachelor’s Degree", "Bachelor’s Degree"),
            ("Master’s Degree", "Master’s Degree"),
            ("Doctorate/PhD", "Doctorate/PhD"),
            ("Other", "Other"),
        ],
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Community Person"
        verbose_name_plural = "Community Person"


class Dwelling(models.Model):
    trust_region = models.ForeignKey(
        TrustRegion,
        on_delete=models.SET_NULL,
        null=True,
        related_name="dwellings_by_trust_region",
        verbose_name="Trust Region",
    )
    trust_village = models.ForeignKey(
        TrustVillage,
        on_delete=models.SET_NULL,
        null=True,
        related_name="dwellings_by_trust_village",
        verbose_name="Trust Village",
    )
    dwelling_number = models.PositiveIntegerField(
        "Dwelling Number",
        validators=[MinValueValidator(1), MaxValueValidator(999)],
    )
    dwelling_type = models.CharField(
        "Dwelling Type",
        max_length=255,
        blank=True,
        choices=[
            ("Permanent", "Permanent"),
            ("Semi-Permanent", "Semi-Permanent"),
            ("Traditional", "Traditional"),
        ],
    )
    construction_year = models.PositiveIntegerField(
        "Construction Year",
        blank=True,
        validators=[MinValueValidator(1900), MaxValueValidator(datetime.now().year)],
    )

    def __str__(self):
        return str(self.dwelling_number)

    class Meta:
        verbose_name = "Dwelling"
        verbose_name_plural = "Dwellings"
        unique_together = [("trust_village", "dwelling_number")]


class Household(models.Model):
    trust_region = models.ForeignKey(
        TrustRegion,
        on_delete=models.SET_NULL,
        null=True,
        related_name="households_by_trust_region",
        verbose_name="Trust Region",
    )
    trust_village = models.ForeignKey(
        TrustVillage,
        on_delete=models.SET_NULL,
        null=True,
        related_name="households_by_trust_village",
        verbose_name="Trust Village",
    )
    dwelling_number = models.ForeignKey(
        Dwelling,
        on_delete=models.SET_NULL,
        null=True,
        related_name="households",
        verbose_name="Dwelling Number",
    )
    household_number = models.PositiveIntegerField(
        "Household Number",
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(999)],
    )
    head_of_household = models.ForeignKey(
        "CommunityPerson",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="household_by_head_of_household",
        verbose_name="Head of Houshold",
    )
    primary_income_source = models.CharField(
        "Primary Income Source", blank=True, max_length=255
    )

    @property
    def member_count(self):
        if hasattr(
            self,
            "household_by_head_of_household" and self.household_by_head_of_household,
        ):
            member_count = self.household_by_head_of_household.count()
            return member_count

        return None

    def __str__(self):
        return str(self.household_number)

    class Meta:
        verbose_name = "Household"
        verbose_name_plural = "Households"
        unique_together = [("trust_village", "dwelling_number", "household_number")]


class HouseholdBankAccount(models.Model):
    account_name = models.CharField(
        "Account Name",
        max_length=255,
        help_text="Enter No Account if household doesn't have bank account.",
    )
    account_number = models.CharField(
        "Account Number",
        max_length=10,
        validators=[MinValueValidator(8), MaxValueValidator(10)],
        help_text="Enter ten digits of 9 if household doesn't have bank account.",
    )
    bank_initials = models.ForeignKey(
        Bank,
        on_delete=models.SET_NULL,
        null=True,
        related_name="household_bank_accounts_by_bank_initials",
        verbose_name="Bank Initials",
        help_text="Choose Nil if household doesn't have bank account.",
    )
    branch = models.CharField(
        "Branch",
        max_length=255,
        blank=True,
        help_text="Leave blank if household doesn't have bank account.",
    )
    status = models.CharField(
        "Status",
        max_length=10,
        blank=True,
        choices=[("Active", "Active"), ("Dormant", "Dormant"), ("Nil", "Nil")],
        help_text="Choose Nil if household doesn't have bank account.",
    )
    household = models.ForeignKey(Household, on_delete=models.SET_NULL, null=True)

    def clean(self):
        if len(self.account_number) != self.bank_initials.account_number_length:
            raise ValidationError(
                f"Account number for {self.bank_initials} should be {self.bank_initials.account_number_length} digits long"
            )

    class Meta:
        verbose_name = "Household Bank Account"
        verbose_name_plural = "Household Bank Accounts"
