
from django.urls import path, include
from event.views import RegisterView, LoginView, EventView, RSVPView, ReviewView

urlpatterns = [
    path('register/',RegisterView.as_view()),
    path('login/',LoginView.as_view()),
    path('event/',EventView.as_view()),
    path('event/<int:pk>/',EventView.as_view()),
    path('event/<int:pk>/rsvp/',RSVPView.as_view()),
    path('event/<int:pk>/rsvp/<int:user_id>/',RSVPView.as_view()),
    path('event/<int:pk>/review/',ReviewView.as_view()),

]