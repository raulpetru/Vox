from django.urls import path

from app_transcription import views
from app_transcription.api import api


urlpatterns = [
    path('', views.RecordingsListView.as_view(), name='dashboard'),
    path('upload_recording/', views.RecordingCreateView.as_view(), name='upload_recording'),
    path('detail_recording/<int:pk>', views.RecordingDetailView.as_view(), name='detail_recording'),
    path('delete_recording/<int:pk>', views.RecordingDeleteView.as_view(), name='delete_recording'),
    path('create_api_client/', views.APIClientCreateView.as_view(), name='create_api'),
    path('api_clients_list/', views.APIClientListView.as_view(), name='api_clients_list'),
    path('delete_api_client/<int:pk>', views.APIClientDeleteView.as_view(), name='delete_api_client'),

    path('api/', api.urls),
]
