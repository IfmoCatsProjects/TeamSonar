from django.urls import path
from .views import collide, main, matches, SuggestionsView

urlpatterns = [
    path('collide', collide, name='collide'),
    path('suggestions/', SuggestionsView.as_view()),
    path('matches', matches),
    path('', main)
]
