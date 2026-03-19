from django import forms
from .models import Faction, Character


# Name Formatter - remove empty spaces and capitalize
def format_name(value):
    return value.strip().title()


# Faction Form
class FactionForm(forms.ModelForm):
    class Meta:
        model = Faction
        fields = ["name"]

    def clean_name(self):
        name = self.cleaned_data["name"]
        return format_name(name)


# Character Form
class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = ["name", "role", "faction", "mentor"]

    def clean_name(self):
        name = self.cleaned_data["name"]
        return format_name(name)

    def clean_role(self):
        role = self.cleaned_data["role"]
        return format_name(role)
