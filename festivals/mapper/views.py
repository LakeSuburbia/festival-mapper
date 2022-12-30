from django.shortcuts import render

from mapper.forms import AddFestivalForm, AddArtistForm, AddArtistToFestivalForm
from mapper.models import Festival, Artist


# Create your views here.
def index(request):
    return list_festivals(request)


def add_festival(request):
    if request.method == "POST":
        form = AddFestivalForm(request.POST)
        if form.is_valid():
            form.save()
            festival = Festival.objects.get(
                name=form.cleaned_data["name"],
                location=form.cleaned_data["location"],
                start_date=form.cleaned_data["start_date"],
                end_date=form.cleaned_data["end_date"],
            )
            return view_festival(request, festival.id)
    form = AddFestivalForm()
    return render(request, "mapper/add_festival.html", {"form": form})


def add_artist(request):
    if request.method == "POST":
        form = AddArtistForm(request.POST)
        if form.is_valid():
            form.save()
            artist = Artist.objects.get(name=form.cleaned_data["name"])
            return view_artist(request, artist.id)
    form = AddArtistForm()
    return render(request, "mapper/add_artist.html", {"form": form})


def add_artist_to_festival(request):
    if request.method == "POST":
        form = AddArtistToFestivalForm(request.POST)
        if form.is_valid():
            form.save()
            return view_festival(request, form.cleaned_data["festival"].id)
    form = AddArtistToFestivalForm()
    return render(request, "mapper/add_artist_to_festival.html", {"form": form})


def view_festival(request, id):
    festival = Festival.objects.get(id=id)
    return render(request, "mapper/view_festival.html", {"festival": festival})


def view_artist(request, id):
    artist = Artist.objects.get(id=id)
    return render(request, "mapper/view_artist.html", {"artist": artist})


def list_festivals(request):
    festivals = Festival.objects.all()
    return render(request, "mapper/list_festivals.html", {"festivals": festivals})


def list_artists(request):
    artists = Artist.objects.all()
    return render(request, "mapper/list_artists.html", {"artists": artists})
