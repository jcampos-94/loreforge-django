from django.shortcuts import render, redirect
from .models import Faction, Character
from .forms import FactionForm, CharacterForm


# Faction view
def factions_list(request):
    factions = Faction.objects.all()
    return render(request, "loreforge/factions.html", {"factions": factions})


# Faction Form view
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


# Character Form view
def add_character(request):
    if request.method == "POST":
        form = CharacterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("characters_list")
    else:
        form = CharacterForm()

    return render(request, "loreforge/add_character.html", {"form": form})
