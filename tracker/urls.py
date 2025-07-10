from django.urls import path
from .views import bug_list_api

urlpatterns = [
    path('api/bugs/', bug_list_api, name='bug_list_api'),
]
