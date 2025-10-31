from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import AuthenticationFailed
from .models import UserProfile, Events, RSVP, Review


# REGISTER SERIALIZER 
#-------------AUTHENTICATION---------------
class RegisterSerializer(serializers.Serializer):
    
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField()
    bio = serializers.CharField()
    location = serializers.CharField()
    profile_picture = serializers.ImageField(required= False)

    def validate(self, data):

        if User.objects.filter(username = data['username']).exists():
            raise serializers.ValidationError('username is taken')
        
        return data
    

    def create(self, validated_data):
        bio = validated_data.pop('bio', '')
        location = validated_data.pop('location', '')
        profile_picture = validated_data.pop('profile_picture', None)


        user = User.objects.create(first_name = validated_data['first_name'], 
                last_name = validated_data['last_name'],
                username = validated_data['username'])
        user.set_password(validated_data['password'])
        user.save()

        UserProfile.objects.create(
            user = user,
            bio = bio,
            location = location,
            profile_picture = profile_picture
        )

        return user
    
# LOGIN SERIALIZER AND JWT 
#------------------------------------------------------------    
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        if not User.objects.filter(username = data['username']).exists():
            raise serializers.ValidationError('Account not found..')
    
        return data   

    def get_jwt_token(self, data):
        
        user = authenticate(username = data['username'], password = data['password'])

        if not user :
            return{
                'message': 'Invalid credentials',
                'data': {}
            }
        refresh = RefreshToken.for_user(user)

        return{
            'message': 'Login Successfully',
            'data':{'token':  { 'refresh': str(refresh),'access': str(refresh.access_token)}
        }} 
        
#----------------EVENT SERIALIZER-------------------------------------------

class EventSerializer(serializers.ModelSerializer):
    organizer = serializers.CharField(source = 'organizer.username', read_only = True)
    class Meta:
        model = Events
        exclude = ['created_at', 'updated_at']

class RSVPSerializer(serializers.ModelSerializer):
    event_title = serializers.CharField(source = 'event.title', read_only = True)
    username = serializers.CharField(source = 'user.username', read_only = True)
    class Meta:
        model = RSVP
        fields = '__all__'
        read_only_fields = ['user', 'event']   

class ReviewSerializer(serializers.ModelSerializer):
    event_title = serializers.CharField(source = 'event.title', read_only = True)
    username = serializers.CharField(source = 'user.username', read_only = True)
    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ['user', 'event']               