from django.urls import path
from . import views

urlpatterns = [
    path('', views.main),
    path('suggestions', views.SuggestionsView.as_view()),
    path('collide', views.collide, name='collide')
]
