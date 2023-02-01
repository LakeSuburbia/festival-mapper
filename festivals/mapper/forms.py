from django import forms
from mapper.models import Festival, Artist, FestivalArtist

from django.core.exceptions import ValidationError


class AddFestivalForm(forms.ModelForm):
    class Meta:
        model = Festival
        fields = ["name", "start_date", "end_date", "location"]
        widgets = {
            "start_date": forms.DateInput(attrs={"type": "date"}),
            "end_date": forms.DateInput(attrs={"type": "date"}),
        }
        labels = {
            "name": "Festival Name",
            "start_date": "Start Date",
            "end_date": "End Date",
            "location": "Location",
        }

    def __init__(self, *args, **kwargs):
        super(AddFestivalForm, self).__init__(*args, **kwargs)

        self.fields["name"].required = True
        self.fields["start_date"].required = True
        self.fields["end_date"].required = True
        self.fields["location"].required = True
        return super(AddFestivalForm, self).__init__(*args, **kwargs)


class AddArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Artist Name"}),
        }
        labels = {
            "name": "Artist Name",
        }


class AddArtistToFestivalForm(forms.ModelForm):
    class Meta:
        model = FestivalArtist
        fields = ["festival", "artist", "date"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date"}),
        }
        labels = {
            "festival": "Festival",
            "artist": "Artist",
            "date": "Date",
        }

    def __init__(self, *args, **kwargs):
        super(AddArtistToFestivalForm, self).__init__(*args, **kwargs)

        self.fields["festival"].required = True
        self.fields["artist"].required = True
        self.fields["date"].required = True
        return super(AddArtistToFestivalForm, self).__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super(AddArtistToFestivalForm, self).clean()
        festival = cleaned_data.get("festival")
        artist = cleaned_data.get("artist")
        date = cleaned_data.get("date")

        if festival and artist and date:
            if FestivalArtist.objects.filter(
                festival=festival, artist=artist, date=date
            ).exists():
                raise ValidationError("Artist already added to festival on that date.")

            if FestivalArtist.objects.filter(festival=festival, artist=artist).exists():
                raise ValidationError(
                    "Artist already added to festival on a different date."
                )

            if not artist.is_available(date):
                raise ValidationError("Artist already plays another show on that date.")

            if festival.start_date > date or festival.end_date < date:
                raise ValidationError(
                    "Date is outside of festival dates."
                    "The festival dates are: {} - {}".format(
                        festival.start_date, festival.end_date
                    ),
                )

        return cleaned_data


class AddMultipleArtistsToFestivalFormSet(forms.BaseFormSet):
    def __init__(self, *args, **kwargs):
        festival = kwargs.pop("festival", None)
        artist = kwargs.pop("artist", None)

        super(AddMultipleArtistsToFestivalFormSet, self).__init__(*args, **kwargs)
        for form in self.forms:
            form.fields["festival"].required = True
            form.fields["artist"].required = True
            form.fields["date"].required = True
            if festival:
                form.fields["festival"].initial = festival
                form.fields["festival"].required = False
                form.fields["festival"].disabled = True
            if artist:
                form.fields["artist"].initial = artist
                form.fields["artist"].required = False
                form.fields["artist"].disabled = True

    def save(self, commit=True):
        instances = []
        for form in self.forms:
            if form.cleaned_data:
                instances.append(form.save(commit=commit))
        return instances
