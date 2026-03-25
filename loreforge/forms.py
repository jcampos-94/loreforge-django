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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # No mentor option until faction is selected
        self.fields["mentor"].queryset = Character.objects.none()

        if "faction" in self.data:
            try:
                faction_id = int(self.data.get("faction"))
                self.fields["mentor"].queryset = Character.objects.filter(
                    faction_id=faction_id
                )
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            # For editing existing character
            # Ensure only mentors from same faction show
            self.fields["mentor"].queryset = self.instance.faction.members.all()

    def clean_name(self):
        name = self.cleaned_data["name"]
        return format_name(name)

    def clean_role(self):
        role = self.cleaned_data["role"]
        return format_name(role)
