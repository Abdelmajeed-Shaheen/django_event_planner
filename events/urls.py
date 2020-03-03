from django.urls import path
from .views import *

urlpatterns = [
	path('', home, name='home'),
    path('signup/', Signup.as_view(), name='signup'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', Logout.as_view(), name='logout'),
	path('event/list', event_list, name='event-list'),
	path('profile/update', profile_update, name='profile-update'),
	path('organizer/<int:organizer_id>/event/list', organizer_event_list, name='organizer-events'),
	path('follow/<int:organizer_id>', follow_organizer, name='follow'),
	path('unfollow/<int:organizer_id>', unfollow_organizer, name='unfollow'),
	path('event/organizer/list', organizer_list, name='organizer-list'),
	path('event/profile/list', profile_list, name='profile-list'),
    path('event/<int:event_id>/detail', event_detail, name='event-detail'),
    path('event/<int:event_id>/update', event_update, name='event-update'),
	path('event/<int:event_id>/delete', event_delete, name='event-delete'),
	path('event/<int:event_id>/book', booking_tickets, name='event-book'),
	path('event/create', event_create, name='event-create'),
    path('dashboard/', dashboard, name='dashboard'),
    path('user/<int:user_id>', asgin_organizer, name='asgin'),
]
