from django import forms
from mapper.models import Festival, Artist, FestivalArtist


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


class AddArtistToFestivalForm(forms.Form):
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
