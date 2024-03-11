from django.urls import path

from . import views

from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    #path("",views.main,name="main"),
    path('',views.main,name='main'),
    path("login",views.login_view,name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("event/<str:id>",views.show_event,name="event"),
    path("create/",views.create_event,name='create_event'),
    path("comment/<str:id>",views.comment,name="comment"),
    path("club/<str:name>",views.club,name="club"),
    path('watchlist/<str:id>',views.watchlist,name="watchlist"),
    path('unactive/<str:id>',views.unactive,name="unactive"),
    path("subscribe/<str:id>",views.subscribe,name="subscribe"),
    path("profile",views.profile,name="profile"),
    path('update',views.update,name="update"),
    path('team/<str:name>',views.team_building,name="team"),
    path("filter/",views.main_filter,name="filter")
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)