from django.urls import path
from mapper.views import (
    index,
    add_festival,
    add_artist,
    add_artist_to_festival,
    view_festival,
    view_artist,
    list_festivals,
    list_artists,
)

urlpatterns = [
    path("", index),
    path("festivals/add", add_festival, name="add_festival"),
    path("artists/add", add_artist, name="add_artist"),
    path("add_artist_to_festival", add_artist_to_festival),
    path("festivals/<id>", view_festival, name="view_festival"),
    path("artists/<id>", view_artist, name="view_artist"),
    path("festivals", list_festivals),
    path("artists", list_artists),
]
