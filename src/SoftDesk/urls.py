from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib import admin
from django.urls import path, include

from TrackingSystem.views import RegisterApi

router = routers.SimpleRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(router.urls)),
    path('signup/', RegisterApi.as_view(), 'signup'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]
