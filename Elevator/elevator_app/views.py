from rest_framework import viewsets , status
from rest_framework.decorators  import action
from rest_framework.response import Response  
from .models import Elevator
from .models import userRequest
from .models import ElevatorSystem
from .serializers import ElevatorSerializer
from .serializers import userRequestSerializer

class ElevatorViewSet(viewsets.ModelViewSet):
    queryset = Elevator.objects.all()
    serializer_class = ElevatorSerializer

    @action(detail=True, methods=['get'])
    def next_destination_floor(self, request, pk=None):
        elevator = self.get_object()
        # Implement logic to determine the next destination floor for the elevator
        # For simplicity, we assume the next floor is just the current floor + 1
        next_floor = elevator.current_floor + 1
        return Response({'destination_floor': next_floor})

    @action(detail=True, methods=['get'])
    def moving_direction(self, request, pk=None):
        elevator = self.get_object()
        # Implement logic to check if the elevator is moving up or down
        # If the elevator's direction is 'stopped', consider it as not moving
        moving_direction = elevator.direction if elevator.direction != 'stopped' else None
        return Response({'direction': moving_direction})

class userRequestViewSet(viewsets.ModelViewSet):
    queryset = userRequest.objects.all()
    serializer_class = userRequestSerializer

    def create(self, request, *args, **kwargs):
        # Override the default create method to handle user requests
        # Implement logic to assign an elevator to the user request
        # You can use the ElevatorSystem class to assign an elevator
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        elevator_system = ElevatorSystem(Elevator.objects.all())  # Initialize ElevatorSystem
        assigned_elevator = serializer.instance.assign_elevator(elevator_system.elevators)
        if assigned_elevator:
            assigned_elevator.is_available = False
            assigned_elevator.save()
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @action(detail=True, methods=['post'])
    def mark_maintenance(self, request, pk=None):
        # Implement logic to mark an elevator as not working or in maintenance
        # You can use the Elevator model's method here or the ElevatorSystem class
        try:
            elevator = Elevator.objects.get(pk=pk)
            elevator.operational_status = False
            elevator.save()
            return Response(status=status.HTTP_200_OK)
        except Elevator.DoesNotExist:
            return Response({'error': 'Elevator not found'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def open_door(self, request, pk=None):
        elevator = self.get_object()
        # Implement logic to open the elevator door
        # For simplicity, we assume that opening the door just sets the 'door_status' to 'open'
        elevator.door_status = 'open'
        elevator.save()
        return Response(status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def close_door(self, request, pk=None):
        elevator = self.get_object()
        # Implement logic to close the elevator door
        # For simplicity, we assume that closing the door just sets the 'door_status' to 'closed'
        elevator.door_status = 'closed'
        elevator.save()
        return Response(status=status.HTTP_200_OK)
