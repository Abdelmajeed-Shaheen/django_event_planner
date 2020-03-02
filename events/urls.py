from django.urls import path
from .views import *

urlpatterns = [
	path('', home, name='home'),
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
	path('event/list', event_list, name='event-list'),
	path('event/profile/list', profile_list, name='profile-list'),
    path('event/<int:event_id>/detail', event_detail, name='event-detail'),
    path('event/<int:event_id>/update', event_update, name='event-update'),
	path('event/<int:event_id>/delete', event_delete, name='event-delete'),
	path('event/<int:event_id>/book', booking_tickets, name='event-book'),
	path('event/create', event_create, name='event-create'),
    path('dashboard/', dashboard, name='dashboard'),
]
