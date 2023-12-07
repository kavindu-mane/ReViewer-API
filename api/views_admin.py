from rest_framework.views import APIView
from . models import User
from . serializers_admin import UserAccountSerializer
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import  permission_classes
from rest_framework.permissions import IsAuthenticated

@permission_classes([IsAuthenticated])
class getUsers(APIView):
    def post(self,request):
        if request.user.is_superuser:
            active = request.data["status"]
            users = User.objects.filter(is_superuser=0 , is_active=(active == "active"))
            serializer = UserAccountSerializer(users , many = True)
            return Response(serializer.data)
        else:
            raise PermissionDenied({"details":"You don't have permission to this action."})