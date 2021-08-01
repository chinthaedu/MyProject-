from django.urls import path
from App import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as v
from django.conf.urls import url
from django.views.static import serve
  

urlpatterns=[
	path('',views.home,name="home"),
	path('addsong/',views.addsong,name='add'),
	path('playsong/<int:sid>/<int:mid>/',views.playsong,name="playsong"),
	path('nextsong/<int:sid>/<int:mid>/',views.nextsong,name="nextsong"),
	path('prevsong/<int:sid>/<int:mid>/',views.prevsong,name="prevsong"),
	path('addmovie/',views.addMovie,name='addmovie'),
	path('moviesList/<int:id>/',views.moviesList,name="moviesList"),
	path('updatesong/<int:id>/',views.updatesong,name="updatesong"),
	path('deletesong/<int:id>/',views.deletesong,name="deletesong"),
	path('rg/',views.usrreg,name="reg"),
	path('login/',v.LoginView.as_view(template_name="ht1/login.html"),name="login"),
	path('logout/',v.LogoutView.as_view(template_name="ht1/logout.html"),name="lgo"),
	path('roltype/',views.rolereq,name="rlrq"),
	path('gvper/',views.gveperm,name='gvpm'),
	path('gvup/<int:t>/',views.gvupdate,name="gvup"),
	path('deleteuser/<int:id>/',views.deleteuser,name="deleteuser"),
	path('pfle/',views.pfle,name="pf"),
	path('pfupd/',views.pfleupd,name="pfup"),
	path('profileupdate/<int:id>/',views.profileUpdate,name="profileupdate"),
	path('fdb/',views.feedback,name="fd"),
	path('chge/',views.changepwd,name="chpd"),
	path('deletemovie/<int:id>/',views.deletemovie,name='deletemovie'),
	path('updatemovie/<int:id>/',views.updatemovie,name='updatemovie'),
	path('moviesongslist/<int:mid>/',views.moviesongslist,name='moviesongslist'),
	path('favourites/',views.favourites,name="favourites"),
	path('addFavourites/<int:sid>/',views.addFavourites,name="addFavourites"),
	path('removeFavourites/<int:sid>/',views.removeFavourites,name="removeFavourites"),
	path('recent/',views.recent,name="recent"),
	path('removeRecents/<int:sid>/',views.removeRecents,name="removeRecents"),
	path('clearAllRecents/',views.clearAllRecents,name="clearAllRecents"),
	path('sub/',views.sub,name="sub"),
	path('sublist/',views.sublist,name="sublist"),

	url(r'^download/(?P<path>.*)$',serve,{'document_root':'settings.MEDIA_ROOT'}),

]

if settings.DEBUG:
	urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
	urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)