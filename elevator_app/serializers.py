from rest_framework import serializers
from .models import Elevator
from .models import userRequest
from .models import ElevatorSystem

#serializer for Elevator model
class ElevatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Elevator
        fields = '__all__'

#serializer for ElevatorSystem model
class ElevatorsystemSerializer(serializers.ModelSerializer):
    class Meta:
        model  = ElevatorSystem
        fields =  '__all__'

#serializer for userRequest model
class userRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = userRequest
        fields = '__all__'