from django.urls import path
from . import views

urlpatterns = [
    path("factions/", views.factions_list, name="factions_list"),
    path("characters/", views.characters_list, name="characters_list"),
]
