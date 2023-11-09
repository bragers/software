from django.urls import path
from . import views

app_name = "polls"
urlpatterns = [
    path("", views.IndexView.as_view(), name="index"),
    path("filter/", views.IndexView.as_view(), name="filter"),  # A common URL for filtering
    path("for_kids/", views.IndexView.as_view(), name="for_kids_filter"),
    path("high_activity/", views.IndexView.as_view(), name="high_activity_filter"),
    path('question_detail/<int:pk>/', views.IndexView.as_view(), name='question_detail'),

]
