from rest_framework import serializers
from events.models import Event, Ticket, Follow
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields =['username']

class EventsSerializer(serializers.ModelSerializer):
    organizer = UserSerializer()
    class Meta:
        model = Event
        fields= '__all__'


class CreateEventsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        exclude= ['organizer']

class BookerSerializer(serializers.ModelSerializer):
    booker = UserSerializer()
    class Meta:
        model = Ticket
        fields = ['booker','number_of_tickets']

class BookedEventsSerializer(serializers.ModelSerializer):
    event = EventsSerializer()
    class Meta:
        model = Ticket
        fields = ['event']

class CreateBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields= ['number_of_tickets']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username','first_name','last_name', 'password', 'email']
    def create(self, validated_data):
        new_user = User(**validated_data)
        new_user.set_password(validated_data.get("password"))
        new_user.save()
        return validated_data

class ListofOrganizers(serializers.ModelSerializer):
    organizer=UserSerializer()
    class Meta:
        model = Follow
        fields = ['organizer']
