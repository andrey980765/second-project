from django.urls import path
from . import views

app_name = 'planner'
urlpatterns = [
    path('', views.index, name='index'),
    path('event/<int:pk>/', views.event_detail, name='event_detail'),
    path('settings/', views.settings_view, name='settings'),
    path('event/add/', views.event_create, name='event_create'),
    path('event/<int:pk>/edit/', views.event_edit, name='event_edit'),
    path('event/<int:pk>/delete/', views.event_delete, name='event_delete'),

    # уведомления
    path("notifications/list/", views.notifications_list, name="notifications_list"),
    path("notifications/poll/", views.notifications_poll, name="notifications_poll"),
    path("notifications/mark_seen/", views.notifications_mark_seen, name="notifications_mark_seen"),
    path("notifications/delete_all/", views.notifications_delete_all, name="notifications_delete_all"),
    path("notifications/mark_all/", views.mark_all_read, name="mark_all_read"),
]
