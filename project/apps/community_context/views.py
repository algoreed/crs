from django.shortcuts import render
from dal import autocomplete
from .models import Dwelling

# Create your views here.


class DwellingAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Dwelling.objects.all().order_by("dwelling_number")

        if self.q:
            qs = qs.filter(dwelling_number__icontains=self.q)

        return qs
