from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from . serializers import UserSerializer
from . models import User

@api_view(['GET'])
def getRoutes(request):
    routes = [
        "api/register",
        "api/login",
        "api/login/refresh",

    ]
    return Response(routes)

class RegisterView(APIView):
    def post(self,request):
        try:
            email = request.data["email"]
            password = request.data['password']
            user = User.objects.filter(email=email).first()

            # check email already exist or not
            if user is not None:
                return Response({
                "email" : "This email already registered"
            })

            # check password length 
            if len(password) < 8:
                return Response({
                "email" : "Password is too short"
            })
            
            serializer = UserSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({
                "details" : "success"
            })
        except KeyError:
            return Response({
                "details":"error"
            })
    
class LoginView(APIView):
    def post(self , request):
        try:
            email = request.data["email"]
            password = request.data["password"]
            user = User.objects.filter(email=email).first()

            if user is None:
                raise AuthenticationFailed("User not found")
            
            if not user.check_password(password):
                raise AuthenticationFailed("Incorrect password")
            
            refresh = RefreshToken.for_user(user)
            return Response({
                "detail":"success",
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        except KeyError:
            return Response({
                "details":"error"
            })
