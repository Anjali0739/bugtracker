from django.urls import path
from .views import bug_list_api, update_bug_status

urlpatterns = [
    path('api/bugs/', bug_list_api, name='bug_list_api'),
    path('api/bugs/<int:bug_id>/', update_bug_status, name='update_bug_status'),
]
