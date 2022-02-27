from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib import admin
from django.urls import path, include

from TrackingSystem.views import RegisterApi, ProjectViewSet, ContributorsViewSet

projects_router = routers.SimpleRouter(trailing_slash=False)
projects_router.register(r"projects/?", ProjectViewSet)
users_router = routers.NestedSimpleRouter(projects_router, r"projects/?", lookup="projects", trailing_slash=False)
users_router.register(r"users/?", ContributorsViewSet, basename="users")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(projects_router.urls)),
    path('', include(users_router.urls)),
    path('signup/', RegisterApi.as_view()),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]
