from django.urls import path
from .views import hello_world
from rest_framework_jwt.views import obtain_jwt_token
from .views import RegisterAPI, LoginAPI, LogoutView, current_user, EventList, EventDetail, get_image, like_image, user_events
from .views import add_or_remove_likes, is_event_liked

urlpatterns = [
    path('api/hello-world/', hello_world, name = 'hello-world'),
    path('api/register/', RegisterAPI.as_view(), name='register'),
    path('api/login/', LoginAPI.as_view(), name='login'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/current_user/', current_user, name = 'current_user'),
    path('api/events/', EventList.as_view(), name='event_list'),
    path('api/events/<int:pk>/', EventDetail.as_view(), name='event_detail'),
    path('api/images/<str:file_name>/',get_image, name='get_image'),
    path('api/like_image/',like_image, name='like_image'),
    path('api/user_events/', user_events, name='user_events'),
    path('api/add_or_remove_likes/', add_or_remove_likes, name='add_or_remove_likes'),
    path('api/is_event_liked/', is_event_liked, name = 'is_event_liked')
]
