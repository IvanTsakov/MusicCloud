from django.conf.urls import url
from . import views 
from django.conf import settings

app_name = 'music'

urlpatterns = [
	#/music/
	url(r'^$', views.index_view, name = 'index'),

	url(r'^logout/$', views.logout, name='logout'),

	url(r'^login/$', views.auth, name='authenticate'),

	url(r'^signup/$', views.UserFormView.as_view(), name='signup'),

	url(r'^search', views.search, name="search"),
	#/music/<album_id>/
	url(r'^album/(?P<pk>[0-9]+)/$', views.detail_view, name = 'detail'),

	url(r'^users/$', views.all_users, name = 'all_users'),

	url(r'^album/(?P<pk>[0-9]+)/favorite/$', views.favorite_album, name = 'favorite_album'),

	url(r'^favorited-albums/$', views.favorited_albums, name = 'favorite_albums'),
	#/music/album/add
	url(r'album/add/$', views.album_create, name='album-add'),

	#music/album/2
	url(r'album/(?P<pk>[0-9]+)/update/$', views.album_update, name='album-update'),

	#music/album/2/delete
	url(r'album/(?P<pk>[0-9]+)/delete/$', views.AlbumDelete.as_view(), name='album-delete'),
	#music/album/2/add-song
	url(r'album/(?P<pk>[0-9]+)/add-song/$', views.album_song_create, name='album-add-song'),

	#music/album/2/song/favorite
	url(r'^songs/(?P<pk>[0-9]+)/favorite/$', views.favorite_song, name='favorite_song'),

	url(r'^songs/(?P<pk>[0-9]+)/favorite-song/$', views.favorite_song_in_songs, name='favorite_in_songs'),
	#music/songs
	url(r'^songs/$', views.songs_view, name='songs'),

	url(r'^song/(?P<pk>[0-9]+)/$', views.song_view, name ='song_view'),

	url(r'songs/favorite-songs/$', views.favorited_songs, name='favorite_songs'),

	#music/album/2/song/delete_song/2/
	url(r'^song/add/$', views.song_create, name='song-add'),

	url(r'^song/(?P<pk>[0-9]+)/update/$', views.song_update, name='song-update'),

	url(r'^song/(?P<pk>[0-9]+)/delete/$', views.delete_song, name='song-delete'),

	url(r'^songs/song/(?P<pk>[0-9]+)/delete-song/$', views.delete_song_in_songs, name='song-delete-in-songs'),
	
]