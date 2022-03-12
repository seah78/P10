from rest_framework_nested import routers
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib import admin
from django.urls import path, include

from TrackingSystem.views import RegisterApi, ProjectViewSet, ContributorsViewSet, IssuesViewSet , CommentsViewSet

projects_router = routers.SimpleRouter(trailing_slash=False)
projects_router.register(r"projects/?", ProjectViewSet)
users_router = routers.NestedSimpleRouter(projects_router, r"projects/?", lookup="projects", trailing_slash=False)
users_router.register(r"users/?", ContributorsViewSet, basename="users")
issues_router = routers.NestedSimpleRouter(projects_router, r"projects/?", lookup="projects", trailing_slash=False)
issues_router.register(r"issues/?", IssuesViewSet, basename= "issues")
comments_router = routers.NestedSimpleRouter(issues_router, r"issues/?", lookup="issues", trailing_slash=False)
comments_router.register(r"comments/?", CommentsViewSet, basename= "comments")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(projects_router.urls)),
    path('', include(users_router.urls)),
    path('', include(issues_router.urls)),
    path('', include(comments_router.urls)),
    path('signup/', RegisterApi.as_view()),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
]
