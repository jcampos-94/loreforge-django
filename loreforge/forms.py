from django import forms
from django.core.exceptions import ValidationError
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
        queryset = Character.objects.all()

        if "faction" in self.data:
            try:
                faction_id = int(self.data.get("faction"))
                filtered = Character.objects.filter(faction_id=faction_id)

                # include currently selected mentor if any
                mentor_id = self.data.get("mentor")
                if mentor_id:
                    queryset = (
                        filtered | Character.objects.filter(id=mentor_id)
                    ).distinct()
                else:
                    queryset = filtered

            except (ValueError, TypeError):
                pass

        self.fields["mentor"].queryset = queryset

    def clean_name(self):
        name = self.cleaned_data["name"]
        return format_name(name)

    def clean_role(self):
        role = self.cleaned_data["role"]
        return format_name(role)

    def clean(self):
        cleaned_data = super().clean()

        name = cleaned_data.get("name")
        faction = cleaned_data.get("faction")
        mentor = cleaned_data.get("mentor")

        # Rule 1: Mentor must be in same faction
        if mentor and faction and mentor.faction != faction:
            self.add_error("mentor", "Mentor must belong to the same faction.")

        # Rule 2: Character cannot mentor themselves
        if mentor and name and mentor.name == name:
            self.add_error("mentor", "A character cannot mentor themselves.")

        # Rule 3 & 4: Prevent circular and deep loops
        if mentor:
            visited = set()
            current = mentor

            while current:
                if current in visited:
                    self.add_error(None, "Circular mentorship detected.")

                if current.name == name:
                    self.add_error(None, "Mentorship loop detected.")

                visited.add(current)
                current = current.mentor

        return cleaned_data
