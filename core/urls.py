from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('chat/', views.chat_view, name='chat'),
    path('missions/', views.missions_view, name='missions'),
    path('night-shift/', views.night_shift_view, name='night_shift'),
    path('hunter/', views.hunter_view, name='hunter'),
    path('council/', views.council_view, name='council'),
    
    # API Endpoints
    path('api/chat/', views.api_chat, name='api_chat'),
    path('api/parallel-chat/', views.api_parallel_chat, name='api_parallel_chat'),
    path('api/mission/', views.api_mission, name='api_mission'),
    path('api/night-shift/', views.api_night_shift, name='api_night_shift'),
    path('api/hunter/', views.api_hunter, name='api_hunter'),
    path('api/council/', views.api_council, name='api_council'),
]
