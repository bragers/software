from django.urls import path
from .views import ArticleListView, process_payment, login_user

app_name = "polls"
urlpatterns = [
    path('articles/', ArticleListView.as_view(), name='article_list'),
    path('articles/for_kids/', ArticleListView.as_view(), {'for_kids': True}, name='article_list_for_kids'),
    path('articles/high_activity/', ArticleListView.as_view(), {'high_activity': True},
         name='article_list_high_activity'),
    path('', ArticleListView.as_view(), name='article_list'),  # This handles the root path
    path('payment/', process_payment, name='process_payment'),
    path('login/', login_user, name='login_user'),
]
