from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from TrackingSystem.serializers import ContributorsSerializer, IssuesSerializer, UserSerializer, RegisterSerializer, ProjectSerializer
from TrackingSystem.models import Contributors, Issues, Project

    
class RegisterApi(GenericAPIView):
    
    serializer_class = RegisterSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "message": "User Created Successfully. Now perform Login to get your token",
            }
        )
        

class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    http_method_names = ["get", "post", "put", "delete"]
    #permission_classes = (IsAuthenticated)


    def create(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data["author"] = request.user.pk
        request.POST._mutable = False
        return super(ProjectViewSet, self).create(request, *args, **kwargs)

    def get_queryset(self):
        return Project.objects.all()
    
    def update(self, request, *args, **kwargs):
        request.POST._mutable = True
        request.data["author"] = request.user.pk
        request.POST._mutable = False
        return super(ProjectViewSet, self).update(request, *args, **kwargs)
    
    
class ContributorsViewSet(ModelViewSet):
    
    queryset = Contributors.objects.all()
    serializer_class = ContributorsSerializer
    http_method_names = ["get", "post", "put", "delete"]

    def get_queryset(self):
        return Contributors.objects.all()
    
    
class IssuesViewSet(ModelViewSet):
    
    queryset = Issues.objects.all()
    serializer_class = IssuesSerializer
    
    def get_queryset(self):
        projects = []
        contributor_projects = Contributors.objects.filter(user = self.request.user.id)
        for project in contributor_projects:
            projects.append(project.project_id)
        author_projects = Project.objects.filter(author = self.request.user.id)
        for project in author_projects:
            projects.append(project.id)
        for project_id in projects:
            if int(project_id) == int(self.kargs['project_pk']):
                return Issues.objects.filter(project__in=self.kwargs['project_pk'])
        return []
            
        