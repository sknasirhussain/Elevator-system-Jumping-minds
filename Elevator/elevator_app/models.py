from django.db import models

#definig the Elevator model by giving it the properties for movement and state detection
class Elevator(models.Model):

    #Defining the number of floors the elevator will have
    Floor_numbers = (
        (1, "First floor"),
        (2, "second foor"),
        (3, "Third floor"),
        (4, "Fourth foor"),
        (5, "Fifth floor"),
        (6, "sixth foor"),
    )
    
    #defining the direction of movement for the elevator
    Directional_choices = (
        ('up', 'Up'),
        ('down', 'Down'),
        ('stopped', 'Stopped'),

    )

    class Meta:
        app_label = 'elevator_app'

    #elevator model has feilds to check if the elevtor is available, the operational status, the floor the elevaor is on and the direction of it's movement
    is_available = models.BooleanField(default=True)
    operational_status = models.BooleanField(default=True)
    current_floor = models.IntegerField(choices = Floor_numbers)
    direction = models.CharField(max_length=10, choices = Directional_choices)

    def __str__(self):
        return f"Elevator {self.pk} - Floor: {self.current_floor}, Direction: {self.direction}"

    def move_up(self):
        if self.current_floor < 6:  # Assuming the top floor is the 6th floor
            self.current_floor += 1
            self.direction = 'up'
            self.save()

    def move_down(self):
        if self.current_floor > 1:  # Assuming the ground floor is the 1st floor
            self.current_floor -= 1
            self.direction = 'down'
            self.save()

    def open_door(self):
        #logic to open the elevator door
        self.door_status = 'open'
        self.save()

    def close_door(self):
        #logic to close the elevator door
        self.door_status = 'closed'
        self.save()

    def start_running(self):
        #logic to start the elevator's operation
        self.operational_status = True
        self.save()

    def stop_running(self):
        #logic to stop the elevator's operation
        self.operational_status = False
        self.save()

    def display_status(self):
        #logic to display the current status of the elevator
        status = f"Elevator {self.pk} - Floor: {self.current_floor}, Direction: {self.direction}, Door: {self.door_status}, Operational Status: {self.operational_status}"
        print(status)
        return status

    def decide_direction(self, user_requests):
        # Implement logic to decide the elevator's direction based on user requests
        # if there are pending user requests, move in that direction
        # If no requests, stay stopped or idle until a request is made
        if not user_requests:
            self.direction = 'stopped'
            self.save()
        else:
            # Determining the direction based on user requests and current floor
            # For simplicity, we would assume the elevator moves in the same direction as the first request
            first_request = user_requests[0]
            if first_request.requested_floor > self.current_floor:
                self.direction = 'up'
            elif first_request.requested_floor < self.current_floor:
                self.direction = 'down'
            else:
                self.direction = 'stopped'
            self.save()

class ElevatorSystem:
    def __init__(self, elevators):
        self.elevators = elevators

    def assign_elevator(self, requested_floor, direction):
        # logic to assign the most optimal elevator to the user request
        # find the elevator that is closest and moving in the same direction
        # If no elevators are available, return None
        closest_elevator = None
        min_distance = float('inf')
    

        for elevator in self.elevators:
            if elevator.is_available:
                if elevator.direction == direction or elevator.direction == 'stopped':
                    distance = abs(elevator.current_floor - requested_floor)
                    if distance < min_distance:
                        closest_elevator = elevator
                        min_distance = distance

        if closest_elevator:
            closest_elevator.is_available = False
            closest_elevator.save()

        return closest_elevator

    def mark_elevator_available(self, elevator_id):
        # Implement logic to mark an elevator as available
        # For example, find the elevator by ID and set 'is_available' to True
        try:
            elevator = Elevator.objects.get(pk=elevator_id)
            elevator.is_available = True
            elevator.save()
        except Elevator.DoesNotExist:
            pass

    def mark_elevator_not_operational(self, elevator_id):
        # Implement logic to mark an elevator as not operational
        # For example, find the elevator by ID and set 'operational_status' to False
        try:
            elevator = Elevator.objects.get(pk=elevator_id)
            elevator.operational_status = False
            elevator.save()
        except Elevator.DoesNotExist:
            pass

class userRequest(models.Model):

    #Defining the floor choices the user will have
    Floor_numbers = (
        (1, "First floor"),
        (2, "second foor"),
        (3, "Third floor"),
        (4, "Fourth foor"),
        (5, "Fifth floor"),
        (6, "sixth foor"),
    )
    
    #Defining the  directional choices the user will have to call the elevator on.
    Directional_choices = (
        ('up', 'Up'),
        ('down', 'Down'),
    )
    
    class Meta:
        app_label = 'elevator_app'

    requested_floor = models.IntegerField(choices = Floor_numbers)
    direction = models.CharField(max_length = 5 , choices = Directional_choices)

    def __str__(self):
        return f"userRequest {self.pk} - Floor: {self.requested_floor}, Direction: {self.direction}"

    def assign_elevator(self, elevators):
        # Implement logic to assign an elevator to this user request
        # Use the ElevatorSystem to find the most optimal elevator for this request
        elevator_system = ElevatorSystem(elevators)
        assigned_elevator = elevator_system.assign_elevator(self.requested_floor, self.direction)

        return assigned_elevator