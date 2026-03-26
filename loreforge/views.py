from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from .models import Faction, Character
from .forms import FactionForm, CharacterForm


# Faction view
def factions_list(request):
    factions = Faction.objects.all()
    return render(request, "loreforge/factions.html", {"factions": factions})


# Add Faction Form view
def add_faction(request):
    if request.method == "POST":
        form = FactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("factions_list")
    else:
        form = FactionForm()

    return render(request, "loreforge/add_faction.html", {"form": form})


# Character view
def characters_list(request):
    characters = Character.objects.select_related("faction", "mentor").all()
    return render(request, "loreforge/characters.html", {"characters": characters})


# Add Character Form view
def add_character(request):
    if request.method == "POST":
        form = CharacterForm(request.POST)
        if form.is_valid():
            character = form.save()

            # If faction has no leader, assign this character
            if not character.faction.leader:
                character.faction.leader = character
                character.role = "Leader"
                character.save()
                character.faction.save()

            return redirect("characters_list")
    else:
        form = CharacterForm()

    return render(request, "loreforge/add_character.html", {"form": form})


# Delete Character Form view
def delete_character(request, character_id):
    character = get_object_or_404(Character, id=character_id)

    if request.method == "POST":
        faction = character.faction

        # Check leadership before deleting
        is_leader = faction.leader == character

        # Delete Character
        character.delete()

        # Get remaining members of faction
        remaining_members = Character.objects.filter(faction=faction)

        if is_leader:
            if not remaining_members.exists():
                # Delete empty faction
                faction.delete()
            else:
                # Promote first member
                new_leader = remaining_members.first()
                faction.leader = new_leader
                new_leader.role = "Leader of the " + faction.name
                new_leader.save()
                faction.save()

        return redirect("characters_list")

    return render(request, "loreforge/delete_character.html", {"character": character})
