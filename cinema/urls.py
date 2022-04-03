from django.urls import path
from . import views
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from MovieApp import settings
from .views import Pwdchangeconfirm, Pwdsentconfirm, Movies, Trending

app_name = 'cinema'

urlpatterns = [
 path('', Movies.as_view()),
 path('movie_details/<movie_id>/', views.movie_details, name='movie_details'),
 path('search/', views.search, name='search'),
 path('signup/', views.signup, name='signup'),
 path('signin/', views.signin, name='signin'),
 path('signout/', views.signout, name='signout'),
 path('movie_details/<int:movie_id>/comments/', views.comments, name='comments'),
 path('posters/', views.posters, name='posters'),
 path('trending/', Trending.as_view()),
 path('movie_details/<int:movie_id>/buy/', views.buy, name='buy'),
 path('profile/changepassword/', views.change, name='change'),
 path('profile/<str:path>/', views.profile, name='profile'),
 path('forgotpassword/', views.forgot, name='forgot'),
 path('passwordsent/', Pwdsentconfirm.as_view()),
 path('passwordchanged/', Pwdchangeconfirm.as_view()),
 path('trending_day/', Movies.as_view()),
 path('top_rated/', views.top_rated,name='top_rated'),
 path('now_playing/', views.now_playing,name='now_playing'),
 path('wishlist/', views.wishlist, name='wishlist'),
 path('wishlist/<int:movie_id>/delete_from_wishlist/', views.delete_from_wishlist, name='delete_from_wishlist'),
 path('movie_details/<int:movie_id>/add_to_wishlist/', views.add_to_wishlist, name='add_to_wishlist'),
 path('delete_poster/<int:image_id>/', views.delete_poster, name='delete_poster'),
 path('recently_browsed/', views.recently_browsed, name='recently_browsed')

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
