from django.urls import path
from . import views

urlpatterns = [
    path('login', views.log_view, name='login'),
    path('reg', views.reg_view),
    path('login-action', views.log),
    path('reg-action', views.register),
    path('', views.auth)
]
