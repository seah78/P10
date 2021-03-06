from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from TrackingSystem.permissions import (
    IsContributorOrAuthorProjectInProjectView,
    IsContributorOrAuthorProjectInContributorView,
    IsContributorOrAuthorProjectInIssueView,
    IsContributorOrAuthorProjectInCommentView,
)
from TrackingSystem.serializers import (
    ContributorsSerializer,
    IssuesSerializer,
    UserSerializer,
    RegisterSerializer,
    ProjectSerializer,
    CommentsSerializer,
)
from TrackingSystem.models import Contributors, Issues, Project, Comments
from django.db.models import Q


class RegisterApi(GenericAPIView):

    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "user": UserSerializer(
                    user, context=self.get_serializer_context()
                ).data,
                "message": ("User Created Successfully.",
                            " Now perform Login to get your token"),
            }
        )


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    http_method_names = ["get", "post", "put", "delete"]
    permission_classes = (IsAuthenticated,
                          IsContributorOrAuthorProjectInProjectView)

    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data["author"] = request.user.pk
        request.POST._mutable = False
        return super(ProjectViewSet, self).create(request, *args, **kwargs)

    def get_queryset(self):
        return Project.objects.filter(
            Q(author=self.request.user.id) | Q(contributors__user=self.request.user.id)
        )

    def update(self, request, *args, **kwargs):
        return super(ProjectViewSet, self).update(request, *args, **kwargs)


class ContributorsViewSet(ModelViewSet):

    queryset = Contributors.objects.all()
    serializer_class = ContributorsSerializer
    http_method_names = ["get", "post", "put", "delete"]
    permission_classes = (
        IsAuthenticated,
        IsContributorOrAuthorProjectInContributorView,
    )

    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data["project"] = self.kwargs["projects_pk"]
        request.POST._mutable = False
        return super(ContributorsViewSet, self).create(request, *args, **kwargs)

    def get_queryset(self):
        return Contributors.objects.filter(project=self.kwargs["projects_pk"])

    def update(self, request, *args, **kwargs):
        return super(ContributorsViewSet, self).update(request, *args, **kwargs)


class IssuesViewSet(ModelViewSet):

    queryset = Issues.objects.all()
    serializer_class = IssuesSerializer
    http_method_names = ["get", "post", "put", "delete"]
    permission_classes = (IsAuthenticated, IsContributorOrAuthorProjectInIssueView)

    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data["project"] = self.kwargs["projects_pk"]
        request.data["author"] = request.user.pk
        request.data["assigned_user"] = request.user.pk

        request.POST._mutable = False
        return super(IssuesViewSet, self).create(request, *args, **kwargs)

    def get_queryset(self):
        return Issues.objects.filter(project=self.kwargs["projects_pk"])

    def update(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data["project"] = self.kwargs["projects_pk"]
        request.data["author"] = request.user.pk
        request.data["assigned_user"] = request.user.pk
        request.POST._mutable = False

        return super(IssuesViewSet, self).update(request, *args, **kwargs)


class CommentsViewSet(ModelViewSet):

    queryset = Comments.objects.all()
    serializer_class = CommentsSerializer
    http_method_names = ["get", "post", "put", "delete"]
    permission_classes = (IsAuthenticated, IsContributorOrAuthorProjectInCommentView)

    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data["author_user_id"] = request.user.pk
        request.data["issue_id"] = self.kwargs["issues_pk"]

        request.POST._mutable = False
        return super(CommentsViewSet, self).create(request, *args, **kwargs)

    def get_queryset(self):
        return Comments.objects.filter(issue_id=self.kwargs["issues_pk"])

    def update(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data["author_user_id"] = request.user.pk
        request.data["issue_id"] = self.kwargs["issues_pk"]
        request.POST._mutable = False
        return super(CommentsViewSet, self).update(request, *args, **kwargs)
