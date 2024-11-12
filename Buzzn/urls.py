from django.urls import path
from . import views

urlpatterns = [
    path('',views.home,name="home"),
    path('profile_list/',views.profile_list,name='profile_list'),
    path('profile/<int:pk>',views.profile,name='profile'),
    path('profile/followers/<int:pk>',views.followers,name='followers'),
    path('profile/follows/<int:pk>',views.follows,name='follows'),
    path('login/',views.login_user,name='login'),
    path('logout/',views.logout_user,name='logout'),
    path('register/',views.register_user,name='register'),
    path('update_user/',views.update_user,name='update_user'),
    path('buzz_like/<int:pk>',views.buzz_like,name='buzz_like'),
    path('buzz_share/<int:pk>',views.buzz_share,name='buzz_share'),
    path('unfollow/<int:pk>',views.unfollow,name='unfollow'),
    path('follow/<int:pk>',views.follow,name='follow'),
    path('delete_buzz/<int:pk>',views.delete_buzz,name='delete_buzz'),
    path('edit_buzz/<int:pk>',views.edit_buzz,name='edit_buzz'),
    path('search/',views.search,name='search'),
    path('search_user/',views.search_user,name='search_user'),
]   