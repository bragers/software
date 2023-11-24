# mysite/urls.py
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('polls.urls')),  # Include your app's URLs at the root level
    # Other URL patterns for your project...
]
