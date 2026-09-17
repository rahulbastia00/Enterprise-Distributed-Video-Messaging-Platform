from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from messaging.views import ChannelListCreateView, MessageListCreateView

urlpatterns = [
    path('admin/', admin.site.urls),
    # JWT Authentication Endpoints
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # REST Messaging Endpoints
    path('api/channels/', ChannelListCreateView.as_view(), name='channel-list'),
    path('api/channels/<int:channel_id>/messages/', MessageListCreateView.as_view(), name='channel-messages'),
]