from __future__ import annotations

import datetime as dt
from collections.abc import Iterator

from django.db import models


class FestivalManager(models.Manager):
    def create_festival_with_artists(
        self, name: str, start_date: dt.date, end_date: dt.date, location: str
    ) -> Festival:
        festival = self.create(
            name=name, start_date=start_date, end_date=end_date, location=location
        )
        return festival

    def get_queryset(self):
        return super(FestivalManager, self).get_queryset().filter(deleted=False)


# Create your models here.
class Festival(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    location = models.CharField(max_length=100)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def dates(self) -> list[dt.date]:
        return [
            date
            for date in (self.start_date + dt.timedelta(n) for n in range(365))
            if date <= self.end_date
        ]

    def get_artists(self) -> list[Artist]:
        return FestivalArtist.objects.filter(festival=self).values_list(
            "artist", flat=True
        )

    def add_artist(self, artist_name: str, date: dt.date) -> None:
        artist = Artist.objects.get_or_create(name=artist_name)[0]
        if not self.start_date <= date <= self.end_date:
            raise ValueError("Date is not in festival range")

        FestivalArtist.objects.create(festival=self, artist=artist, date=date)

    def update_artist(self, artist_name: str, date: dt.date) -> None:
        artist = Artist.objects.get(name=artist_name)
        if not self.start_date <= date <= self.end_date:
            raise ValueError("Date is not in festival range")

        FestivalArtist.objects.filter(festival=self, artist=artist).update(date=date)

    def remove_artist(self, artist_name: str) -> None:
        obj = FestivalArtist.objects.get(festival=self, artist__name=artist_name)
        obj.delete()

    def add_artists(self, artists: list[Artist], date: dt.date) -> None:
        for artist in artists:
            self.add_artist(artist.name, date)

    def available_artists(self) -> Iterator[Artist]:
        for date in self.dates:
            for artist in Artist.objects.filter(available_dates__contains=date):
                yield artist

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()


class ArtistManager(models.Manager):
    def get_queryset(self):
        return super(ArtistManager, self).get_queryset().filter(deleted=False)


class Artist(models.Model):
    name = models.CharField(max_length=100)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    @property
    def available_dates(self) -> list[dt.date]:
        return FestivalArtist.objects.filter(
            artist=self, festival__start_date__lte=dt.date.today()
        ).values_list("date", flat=True)

    @property
    def festivals(self) -> list[Festival]:
        return FestivalArtist.objects.filter(artist=self).values_list(
            "festival", flat=True
        )

    def add_festival(self, festival: Festival, date: dt.date) -> None:
        if not festival.start_date <= date <= festival.end_date:
            raise ValueError("Date is not in festival range")

        FestivalArtist.objects.create(festival=festival, artist=self, date=date)

    def update_festival(self, festival: Festival, date: dt.date) -> None:
        if not festival.start_date <= date <= festival.end_date:
            raise ValueError("Date is not in festival range")

        FestivalArtist.objects.filter(festival=festival, artist=self).update(date=date)

    def remove_festival(self, festival: Festival) -> None:
        obj = FestivalArtist.objects.get(festival=festival, artist=self)
        obj.delete()

    def add_festivals(self, festivals: list[Festival], date: dt.date) -> None:
        for festival in festivals:
            self.add_festival(festival, date)

    def is_available(self, date: dt.date) -> bool:
        return not FestivalArtist.objects.filter(artist=self, date=date).exists()

    def get_available_festivals(self) -> Iterator[Festival]:
        for date in self.available_dates:
            for festival in Festival.objects.filter(
                start_date__lte=date, end_date__gte=date
            ).exclude(pk__in=self.festivals):
                yield festival

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()


class FestivalArtistManager(models.Manager):
    def get_queryset(self):
        return super(FestivalArtistManager, self).get_queryset().filter(deleted=False)


class FestivalArtist(models.Model):
    festival = models.ForeignKey(Festival, on_delete=models.CASCADE)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    date = models.DateField()
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.festival} - {self.artist} - {self.date}"

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.save()

    def restore(self, *args, **kwargs):
        self.deleted = False
        self.save()

    def hard_delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
