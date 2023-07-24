from rest_framework import serializers
from .models import Elevator
from .models import userRequest

class ElevatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Elevator
        fields = '__all__'


class userRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model = userRequest
        fields = '__all__'