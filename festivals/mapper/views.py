from django.shortcuts import render

from django.forms import modelformset_factory, widgets


from mapper.forms import (
    AddFestivalForm,
    AddArtistForm,
    AddMultipleArtistsToFestivalFormSet,
    AddArtistToFestivalForm,
)
from mapper.models import Festival, Artist, FestivalArtist


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


BulkAddArtistFormset = modelformset_factory(
    FestivalArtist,
    fields=("festival", "artist", "date"),
    widgets={
        "date": widgets.DateInput(
            attrs={
                "type": "date",
            },
        ),
    },
    form=AddArtistToFestivalForm,
    formset=AddMultipleArtistsToFestivalFormSet,
)


def add_artists_to_festival(request, festival=None, artist=None):
    if festival:
        festival = Festival.objects.get(id=festival)
    if artist:
        artist = Artist.objects.get(id=artist)

    data = {
        "form-TOTAL_FORMS": "5",
        "form-INITIAL_FORMS": "0",
    }

    messages = []

    if request.method == "POST":
        formset = BulkAddArtistFormset(request.POST, festival=festival, artist=artist)

        if formset and formset.is_valid():
            formset.save()
            if festival:
                return view_festival(request, festival.id)
            if artist:
                return view_artist(request, artist.id)

        messages += formset.errors if formset else []
        messages += formset.non_form_errors() if formset else []

    return render(
        request,
        "mapper/add_artists_to_festival.html",
        {
            "formset": BulkAddArtistFormset(
                data,
                festival=festival,
                artist=artist,
            ),
            "festival": festival,
            "artist": artist,
            "messages": messages,
        },
    )


def view_festival(request, id):
    festival = Festival.objects.get(id=id)
    return render(
        request,
        "mapper/view_festival.html",
        {
            "festival": festival,
        },
    )


def view_artist(request, id):
    artist = Artist.objects.get(id=id)
    return render(request, "mapper/view_artist.html", {"artist": artist})


def list_festivals(request):
    festivals = Festival.objects.all()
    return render(request, "mapper/list_festivals.html", {"festivals": festivals})


def list_artists(request):
    artists = Artist.objects.all()
    return render(request, "mapper/list_artists.html", {"artists": artists})
