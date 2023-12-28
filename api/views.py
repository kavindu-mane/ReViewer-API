from rest_framework.response import Response
from rest_framework.decorators import api_view , permission_classes
from rest_framework.views import APIView
from rest_framework.exceptions import  ParseError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.middleware import csrf
from django.utils import timezone
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import InvalidToken
from . serializers import UserSerializer , AccountSerializer
from . models import User

@api_view(['GET'])
def getRoutes(request):
    routes = [
        "api/register",
        "api/login",
        "api/login/refresh",
        "api/logout",
    ]
    return Response(routes)

# get user tokes for current user
def get_user_tokens(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh_token": str(refresh),
        "access_token": str(refresh.access_token)
    }

# add tokens to cookies
def cookie_adder(response , key , value , expire):
    response.set_cookie(
        key=key,
        value=value,
        expires=expire,
        secure=settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
        httponly=settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
        samesite=settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
    )

    return response

@permission_classes([])
class RegisterView(APIView):
    def post(self,request):
        try:
            email = request.data["email"]
            password = request.data['password']
            conf_password = request.data['confpassword']
            user = User.objects.filter(email=email).first()

            # check email already exist or not
            if user is not None:
                return Response({
                "email" : "This email already registered"
            })

            # check password length 
            if len(password) < 8:
                return Response({
                "password" : "Password is too short"
            })

            # check password and confirm password is same or not
            if password != conf_password:
                return Response({
                "password" : "Password and confirm password mismatch!",
                "confpassword" : "Password and confirm password mismatch!"
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
    
@permission_classes([])
class LoginView(APIView):
    def post(self , request):
        try:
            email = request.data["email"]
            password = request.data["password"]
            user = User.objects.filter(email=email).first()

            if user is None:
                return Response({"details":"Email or password is incorrect!"})
            
            if not user.check_password(password):
                return Response({"details":"Email or password is incorrect!"})
            
            if not user.is_active:
                return Response({"details":"This account is disabled!"})
            
            tokens = get_user_tokens(user)
            res = Response()
            expiration_date = None
            if "remember" in request.data:
                expiration_date = timezone.now() + timezone.timedelta(days=30)
                res = cookie_adder(response=res , 
                            key="remember" , 
                            value=True , 
                            expire=expiration_date
                        )

            res = cookie_adder(response=res , 
                            key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'] , 
                            value=tokens["refresh_token"] , 
                            expire=expiration_date
                        )
            res = cookie_adder(response=res , 
                            key=settings.SIMPLE_JWT['AUTH_COOKIE_CSRF'] , 
                            value=csrf.get_token(request) , 
                            expire=expiration_date
                        )
            res.data = {"detail":"success",
                        "access":tokens["access_token"],
                        "csrf":csrf.get_token(request) ,
                        "status":user.is_superuser}
            res["X-CSRFToken"] = csrf.get_token(request)
            return res
 
        except KeyError:
            return Response({
                "details":"error"
            })

@permission_classes([IsAuthenticated])
class LogoutView(APIView):
    def post(self,request):
        try:
            refreshToken = request.COOKIES.get(
                settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
            token = RefreshToken(refreshToken)
            token.blacklist()

            res = Response()
            res.delete_cookie(settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'])
            res.delete_cookie("csrftoken")
            res.delete_cookie("remember")
            res["X-CSRFToken"]=None
            
            res.data = {"detail":"success"}
            return res
        except:
            raise ParseError("Invalid token")
    
class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = None

    def validate(self, attrs):
        attrs['refresh'] = self.context['request'].COOKIES.get('refresh')
        if attrs['refresh']:
            return super().validate(attrs)
        else:
            raise InvalidToken(
                'No valid token found in cookie refresh')

class CookieTokenRefreshView(TokenRefreshView):
    serializer_class = CookieTokenRefreshSerializer

    @permission_classes([IsAuthenticated])
    def finalize_response(self, request,response, *args, **kwargs):
        if response.data.get("refresh"):
            expiration_date = None
            if request.COOKIES.get("remember" , False):
                expiration_date = timezone.now() + timezone.timedelta(days=30)
                response = cookie_adder(response=response , 
                            key="remember" , 
                            value=True , 
                            expire=expiration_date
                        )
            response = cookie_adder(response=response , 
                            key=settings.SIMPLE_JWT['AUTH_COOKIE_REFRESH'] , 
                            value=response.data['refresh'] , 
                            expire=expiration_date
                        )
            response = cookie_adder(response=response , 
                            key=settings.SIMPLE_JWT['AUTH_COOKIE_CSRF'] , 
                            value=request.COOKIES.get("csrftoken") , 
                            expire=expiration_date
                        )
            response.data = {"detail":"success" ,
                              "access":response.data["access"] ,
                              "csrf":request.COOKIES.get("csrftoken")}

        response["X-CSRFToken"] = request.COOKIES.get("csrftoken")
        return super().finalize_response(request, response ,*args, **kwargs)
 
@permission_classes([IsAuthenticated])
class GetUser(APIView):
    def get(self ,request):
        try:
            user = User.objects.get(email = request.user.email)
        except User.DoesNotExist:
            return Response({"details" : "User not found"})

        serializer = AccountSerializer(user)
        return Response(serializer.data)

@permission_classes([IsAuthenticated])
class WhoIAm(APIView):
    def get(self , request):
        return(Response({
            "details":request.user.is_superuser
        }))