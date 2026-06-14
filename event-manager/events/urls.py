from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('api/events', views.event_list, name='event_list'),
    path('api/events/<int:event_id>', views.event_detail, name='event_detail'),
    path('api/register', views.register_event, name='register_event'),
    path('api/manage-registrations', views.manage_registrations, name='manage_registrations'),
]