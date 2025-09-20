from django.urls import path
from . import views

app_name = 'planner'   # нужно для удобного именования ссылок в шаблонах

urlpatterns = [
    path('', views.index, name='index'),  # главная страница (список событий)
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),  # страница события
    path('settings/', views.settings_view, name='settings'),  # страница настроек
]