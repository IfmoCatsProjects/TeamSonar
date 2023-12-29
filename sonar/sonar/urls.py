from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authcore.urls')),
    path('', include('core.urls'), name='main'),
]
