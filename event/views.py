from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import RegisterSerializer, LoginSerializer, EventSerializer, RSVPSerializer, ReviewSerializer
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Events, RSVP, Review
from django.core.paginator import Paginator
# Create your views here.

class RegisterView(APIView):
    def post(self, request):

        data = request.data
        serializer = RegisterSerializer(data = data)

        if not serializer.is_valid():
            return Response({
                'data': serializer.errors,
                'message': 'Something went wrong'
            }, status= status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return Response({
            'data': {},
            'message': 'your account is created',
        }, status= status.HTTP_201_CREATED)
    

class LoginView(APIView):
    def post(self, request):

        data = request.data
        serializer = LoginSerializer(data = data)

        if not serializer.is_valid():
            return Response({
                'data': serializer.errors,
                'message': 'Something went wrong'
            }, status= status.HTTP_400_BAD_REQUEST)
        
        response = serializer.get_jwt_token(serializer.data)

        return Response(response, status = status.HTTP_200_OK)
    
#-------------------VIEWS FOR EVENTS-----------------
class EventView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]


    def get(self, request, pk = None):

        if pk:
            try:
                event = Events.objects.get(pk = pk)
                serializer = EventSerializer(event)
                return Response({
                    'data': serializer.data,
                    'message': 'Event Fetched Successfully'
                })
            
            except Events.DoesNotExist:
                return Response({
                    'error':'Event not found'
                }, status= status.HTTP_404_NOT_FOUND)
            
        else:    
            events = Events.objects.all()

            page_number = request.GET.get('page', 1)
            paginator = Paginator(events, 2)

            serializer = EventSerializer(paginator.page(page_number), many = True)   

            return Response({
                'data': serializer.data,
                'message': 'All events successfully fetched'
            }, status= status.HTTP_200_OK)



    def post(self, request):

        self.permission_classes = [IsAuthenticated]

        serializer = EventSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
           serializer.save(organizer=request.user)

           return Response({
            'data': serializer.data,
            'message': 'Event created successfully'
        }, status=status.HTTP_201_CREATED)
    
        return Response({'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
    def patch(self, request, pk):
        self.permission_classes = [IsAuthenticated]

        if not request.user or not request.user.is_authenticated:
            return Response({
                'message': 'Authentication required'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        try:
            event = Events.objects.get(pk = pk)

        except Events.DoesNotExist:
            return Response({
                'message': 'Event not found'
            }, status=status.HTTP_404_NOT_FOUND)   

        if event.organizer != request.user:
            return Response({
                'message': 'You are not the organizer of the event'
            }, status=status.HTTP_403_FORBIDDEN) 
        
        serializer = EventSerializer(event, data=request.data, partial=True, context={'request':request})

        if not serializer.is_valid():
            return Response({
                'errors': serializer.errors
            },status= status.HTTP_400_BAD_REQUEST)
        
        serializer.save()

        return Response({
            'data': serializer.data,
            'message': 'Event update Successfully'
        }, status= status.HTTP_200_OK)
    
    def delete(self, request, pk):
        self.permission_classes = [IsAuthenticated]

        try:
            event = Events.objects.get(pk = pk)

        except Events.DoesNotExist:
            return Response({
                'message': 'Event not found'
            }, status=status.HTTP_404_NOT_FOUND) 
        
        if event.organizer != request.user:
            return Response({
                'message': 'You are not the organizer of the event'
            }, status=status.HTTP_403_FORBIDDEN) 
        
        if not request.user or not request.user.is_authenticated:
            return Response({
                'message': 'Authentication required'
            }, status=status.HTTP_401_UNAUTHORIZED)
        
        event.delete()
        return Response({
            'message': 'Event deleted successfully'
        }, status= status.HTTP_200_OK)
    
class RSVPView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, pk):
        try:
            event = Events.objects.get(pk=pk)

        except Events.DoesNotExist:
            return Response({
                'message': 'Event does not exist'
            }, status= status.HTTP_404_NOT_FOUND)    
        
        if RSVP.objects.filter(event=event, user= request.user).exists():
            return Response({
                'message': 'RSVP already exist for this event'
            }, status= status.HTTP_400_BAD_REQUEST) 

        serializer = RSVPSerializer(data = request.data,)

        if serializer.is_valid():
            serializer.save(user = request.user, event = event)
            return Response({
                'data': serializer.data,
                'message': 'RSVP successfully added for this event'
            }, status= status.HTTP_201_CREATED)
        
        return Response({
            'error': serializer.errors
        }, status= status.HTTP_400_BAD_REQUEST) 
    
    def patch(self, request, pk, user_id):
        try:
            rsvp = RSVP.objects.get(pk=pk, user_id=user_id)

        except RSVP.DoesNotExist:
            return Response({
                'message': 'RSVP not found'
            }, status= status.HTTP_404_NOT_FOUND)
        
        if request.user.id != user_id:
            return Response({
                'message': 'You cannot update someone else RSVP'
            }, status= status.HTTP_403_FORBIDDEN)
        
        serializer = RSVPSerializer(rsvp, data= request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'data': serializer.data,
                'message': 'RSVP updated successfully'
            }, status= status.HTTP_200_OK)
        
        return Response({
            'data': serializer.errors,
        }, status= status.HTTP_400_BAD_REQUEST)
    
class ReviewView(APIView):
    permission_classes = [AllowAny]
    authentication_classes = [JWTAuthentication]

    def post(self, request, pk):
        self.permission_classes = [IsAuthenticated]
        try:
            event = Events.objects.get(pk=pk)

        except Events.DoesNotExist:
            return Response({
                'message': 'Event does not exist'
            }, status= status.HTTP_404_NOT_FOUND) 
        
        serializer = ReviewSerializer(data = request.data,)

        if serializer.is_valid():
            serializer.save(user = request.user, event = event)
            return Response({
                'data': serializer.data,
                'message': 'Review successfully added for this event'
            }, status= status.HTTP_201_CREATED)
        
        return Response({
            'error': serializer.errors
        }, status= status.HTTP_400_BAD_REQUEST) 
    
    def get(self, request, pk):
        
        reviews = Review.objects.filter(event__id = pk)

        page_number = request.GET.get('page', 1)
        paginator = Paginator(reviews, 2)

        serializer = ReviewSerializer(paginator.page(page_number), many = True)

        return Response({
            'data': serializer.data,
            'message':'Reviews fetched Successfully'
        }, status=status.HTTP_200_OK)
        

        





        




        
    









