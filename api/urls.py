from django.urls import path
from .views import EventView, Register , BookingView
from rest_framework_simplejwt.views import (
	TokenObtainPairView,
	TokenRefreshView,
)



urlpatterns = [

	path('api/event/list/<int:event_id>', EventView.as_view(), name='api-event-list'),
	path('api/event/list/user/<int:user_id>', EventView.as_view(), name='api-event-list'),
	path('api/event/list', EventView.as_view(), name='api-event-list'),


	path('api/event/booking/<int:event_id>', BookingView.as_view(), name='api-event-booking'),
	path('api/event/booking', BookingView.as_view(), name='api-event-booking'),


	path('api/register', Register.as_view(), name='api-register'),
	path('api/login/', TokenObtainPairView.as_view(), name='api-login'),
	path('api/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
