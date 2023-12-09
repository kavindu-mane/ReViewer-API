from rest_framework.views import APIView
from django.db.models import Q
from . models import User
from . serializers_admin import UserAccountSerializer
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import  permission_classes
from rest_framework.permissions import IsAuthenticated

@permission_classes([IsAuthenticated])
class getUsers(APIView):
    def post(self,request):
        if request.user.is_superuser:
            active = request.data["status"]
            page = request.data["page"]
            search = None;
            if "search" not in request.data or request.data["search"] == "":
                users = User.objects.filter(is_superuser=0 , is_active=(active == "active")).order_by("name")
            else:
                search = request.data["search"]
                users = User.objects.filter((Q(name__icontains=search) | Q(email__icontains=search)) & Q(is_superuser=0)).order_by("name")

            paginator = Paginator(users, 25)
            paginated_users = paginator.get_page(page)
            serializer = UserAccountSerializer(paginated_users , many = True)
            return Response({"users":serializer.data , 
                            "meta":{
                                "count":paginator.count , 
                                "page_count":paginator.num_pages,
                                "start":paginated_users.start_index(),
                                "end":paginated_users.end_index()
                                }
                            })
        else:
            raise PermissionDenied({"details":"You don't have permission to this action."})
        
@permission_classes([IsAuthenticated])
class changeUserStatus(APIView):
    def post(self,request):
        if request.user.is_superuser:
            active = request.data["status"]
            users = User.objects.get(email = request.data["email"])
            users.is_active = (active == "active")
            users.save()
            return Response({
                "details":"success"
            })
        else:
            raise PermissionDenied({"details":"You don't have permission to this action."})