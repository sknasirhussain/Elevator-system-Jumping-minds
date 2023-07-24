from django.urls import path, include
from rest_framework.routers import DefaultRouter
from elevator_app.views import ElevatorViewSet, userRequestViewSet

# Create a router and register our ViewSets with it.
router = DefaultRouter()
router.register(r'elevators', ElevatorViewSet)
router.register(r'user-requests', userRequestViewSet)

# The API URLs are now determined automatically by the router.
urlpatterns = [
    path('', include(router.urls)),
]
