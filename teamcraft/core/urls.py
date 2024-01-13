from django.urls import path
from . import views

urlpatterns = [
    path('sims', views.SuggestionsView.as_view()),
    path('matchess', views.get_matches),
    path('matches', views.main),
    path('messages', views.main),
    path('profile', views.main),
    path('friends', views.main),
    path('', views.main),
]
