from rest_framework import generics
from rest_framework.permissions import AllowAny
from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from django.contrib.auth.views import LoginView
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth import logout, login
from django.views.generic import RedirectView
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
import json
from .serializers import EventSerializer
from .models import Event, Like
import os
from django.http import FileResponse
from django.conf import settings
from django.http import FileResponse
from django.db.models import F
import base64
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
import datetime
from rest_framework import status

# from utils.myutils import convert_rb_format

# Create your views here.
from django.http import JsonResponse

def hello_world(request):
    data = {'message': 'Hello, World!'}
    return JsonResponse(data)

User = get_user_model()

class RegisterAPI(generics.CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        print(request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
        })

class LoginAPI(LoginView):
    def post(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return JsonResponse({'message': 'User is already authenticated.'}, status=200)
        data = json.loads(request.body)
        username = data['username']
        password = data['password']
        
        if username is None or password is None:
            return JsonResponse({'message': 'Invalid username or password.'}, status=400)
        
        user = authenticate(username=username, password=password)
        
        if not user:
            return JsonResponse({'message': 'Invalid username or password.'}, status=400)
        else :
            login(request, user)
        try:
            token, created = Token.objects.get_or_create(user=user)
        except IntegrityError as e:
            print(e)
            return JsonResponse({'message': 'Token creation failed.'}, status=500)
        return JsonResponse({'token': token.key})

class LogoutView(RedirectView):
    url = '/'

    def get(self, request, *args, **kwargs):
        logout(request)
        return super().get(request, *args, **kwargs)

@login_required
def current_user(request):
    
    return JsonResponse({
        "username" : request.user.username,
        "email" : request.user.email,
        "is_authenticated": request.user.is_authenticated,
        "user_id": request.user.id
    })
   
class EventList(generics.ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    def post(self, request, format=None):
        serializer = EventSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EventDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer


def get_image(request, file_name):
    file_path = os.path.join(str(settings.BASE_DIR) + '/images/', file_name)
    print(file_path)
    file_ext = os.path.splitext(file_path)[1]
    content_type = None
    with open(file_path, 'rb') as f:
        image_data = f.read()
    if file_ext == '.jpg' or file_ext == '.jpeg':
        content_type = 'image/jpeg'
    elif file_ext == '.png':
        content_type = 'image/png'
    response = HttpResponse(image_data, content_type = content_type)
    return response

# @method_decorator(csrf_exempt, name='dispatch')
def like_image(request):
    if request.method == 'POST':
       data = json.loads(request.body) 
       event_id = data['event_id']
       user_id = data['user_id']
       event = get_object_or_404(Event, id= event_id)
       user = get_object_or_404(User, id = user_id)
       like = Like(user=user, event=event)
       like.save()
       return JsonResponse({
            'success': True,
            'message': 'Valid'
       })
    else:
        return JsonResponse({
            'success': False,
            'message': 'Invalid'
        })

class DatetimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return super().default(obj)

# @method_decorator(csrf_exempt, name='dispatch')
def user_events(request):
    if request.method == 'GET':
        user = get_object_or_404(User, id=request.user.id)
        events = Event.objects.filter(user=user)
        serialized_events = json.dumps(list(events.values()), cls = DatetimeEncoder)
        return HttpResponse(serialized_events, content_type='application/json')
    else:
        events = Event.objectsj.none()
        serialized_events = json.dumps(list(events.values()), cls=DatetimeEncoder)
        return HttpResponse(serialized_events, content_type='application/json')

@method_decorator(csrf_exempt, name='dispatch')
def add_or_remove_likes(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        like = Like.objects.filter(user_id = request.user.id, event_id = data['event_id'])
        user = get_object_or_404(User,id = request.user.id)
        event = get_object_or_404(Event, id = data['event_id'])
        if like.exists():
            like.delete()
            event.save()
        else:
            user = get_object_or_404(User,id = request.user.id)
            event = get_object_or_404(Event, id = data['event_id'])
            like = Like(user = user, event = event)
            event.save()
            like.save()
        return JsonResponse({
            'success':True,
        })
    else:
        return JsonResponse({
            'success':False,
            'message':'Invalid'
        }, content_type = 'application/json')

def is_event_liked(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user = get_object_or_404(User, id = request.user.id)
        event = get_object_or_404(Event, id = data['event_id'])
        Likes = Like.objects.filter(user = user, event = event) 
        NumLikes = Like.objects.filter(event = event)
        return JsonResponse({
            'success':True,
            'message':'Valid',
            'is_liked': Likes.exists(), 
            'num_likes': len(NumLikes)
        }, content_type = 'application/json')
    else:
        return JsonResponse({
            'success':False,
            'message':'Invalid' 
        }, content_type = 'application/json')