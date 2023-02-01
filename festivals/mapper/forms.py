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
