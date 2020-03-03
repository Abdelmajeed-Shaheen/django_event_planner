from django.shortcuts import render
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework import status
from events.models import Event, Ticket, Follow
from .serializers import (
EventsSerializer,
CreateEventsSerializer,
RegisterSerializer,
BookerSerializer,
BookedEventsSerializer,
CreateBookingSerializer,
ListofOrganizers,
FollowOrganizerSerializer,
)
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOrganizer
from datetime import datetime
from rest_framework.views import APIView


class Register(CreateAPIView):
	serializer_class = RegisterSerializer


class EventView(APIView):
	def get(self,request,event_id=None,user_id=None):
		self.permission_classes = [IsAuthenticated]
		self.check_permissions(request)
		if user_id:
			user = User.objects.get(id=user_id)
			event_obj_list = Event.objects.filter(organizer=user)
			serializer= EventsSerializer(event_obj_list,many=True)
			return Response(serializer.data)
		if event_id:
			event_obj = Event.objects.get(id=event_id)
			serializer= EventsSerializer(event_obj)
			return Response(serializer.data)
		events = Event.objects.filter(date__gte=datetime.today())
		serializer = EventsSerializer(events,many=True)
		return Response(serializer.data)

	def post(self,request):
		self.permission_classes = [IsAuthenticated]
		self.check_permissions(request)
		serializer = CreateEventsSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save(organizer=request.user)
			return Response(serializer.data,status=status.HTTP_201_CREATED)
		return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

	def put(self, request, event_id):
		self.permission_classes=[IsAuthenticated, IsOrganizer]
		event = Event.objects.get(id = event_id)
		self.check_object_permissions(request,event)
		serializer = CreateEventsSerializer(event, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status = status.HTTP_200_OK)
		return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class BookingView(APIView):
	def get(self,request,event_id=None):
		if event_id:
			self.permission_classes = [IsAuthenticated,IsOrganizer]
			event = Event.objects.get(id = event_id)
			self.check_object_permissions(request,event)
			tickets = Ticket.objects.filter(event=event)
			serializer = BookerSerializer(tickets,many=True)
			return Response(serializer.data)
		self.permission_classes = [IsAuthenticated]
		self.check_permissions(request)
		tickets = Ticket.objects.filter(booker=request.user)
		serializer = BookedEventsSerializer(tickets,many=True)
		return Response(serializer.data)

	def post(self,request,event_id):
		self.permission_classes = [IsAuthenticated]
		self.check_permissions(request)
		event = Event.objects.get(id=event_id)
		serializer = CreateBookingSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save(booker=request.user,event=event)
			event.booked_seats += serializer['number_of_tickets'].value
			event.save()
			return Response(serializer.data,status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

class ListofOrganizersView(APIView):
	def get(self, request):
		self.permission_classes = [IsAuthenticated]
		self.check_permissions(request)
		follow_list = Follow.objects.filter(user=request.user)
		serializer=ListofOrganizers(follow_list,many=True)
		return Response(serializer.data)

	def post(self, request, organizer_id):
		self.permission_classes=[IsAuthenticated]
		self.check_permissions(request)
		organizer_obj= User.objects.get(id= organizer_id)
		serializer = FollowOrganizerSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save(user=request.user,organizer=organizer_obj)
			return Response(serializer.data,status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

	def delete(self,request,organizer_id):
		self.permission_classes=[IsAuthenticated]
		self.check_permissions(request)
		organizer_obj= User.objects.get(id= organizer_id)
		follow_obj = Follow.objects.get(user=request.user,organizer=organizer_obj)
		follow_obj.delete()
		return Response(serializer.data,status=status.HTTP_204_NO_CONTENT)
