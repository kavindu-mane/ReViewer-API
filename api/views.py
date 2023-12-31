from rest_framework.response import Response
from rest_framework.decorators import api_view , permission_classes
from rest_framework.views import APIView
from rest_framework.exceptions import  ParseError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.middleware import csrf
from django.utils import timezone
from rest_framework_simplejwt.views import TokenRefreshView
from . serializers import UserSerializer , AccountSerializer , CookieTokenRefreshSerializer
from . models import User

# in this system use JWT tokens for authentications
# for more details about authentication in this project please see authenticate.py custom authentication file.

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

# register view : user registration request comes to this view. this view return success or flagged error for front-end
# serializer : UserSerializer in serializers.py
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

# login view : all users and admin login the system via this view. if user creadential valied this this function do below task.
# create cookies for refresh token , csrf token and remember cookie (if user need remember me function)
# this function return response with access token , csrf and user role is admin or not (if admin , return true otherwise false)
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

# logout view : all users logout via this view. in this view remove all cookies and blacklist current refresh token.
# response task success or if flagged any exception raise parse error
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

# tooken refresh view : this view refresh access and refresh tokens. because access token expire every 5 minute.
# serializer : CookieTokenRefreshSerializer in serializers.py
class CookieTokenRefreshView(TokenRefreshView):
    serializer_class = CookieTokenRefreshSerializer

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
 
# get user view : this view return user basic details.
# serializer : AccountSerializer in serializers.py
@permission_classes([IsAuthenticated])
class GetUserView(APIView):
    def get(self ,request):
        try:
            user = User.objects.get(email = request.user.email)
        except User.DoesNotExist:
            return Response({"details" : "User not found"})

        serializer = AccountSerializer(user)
        return Response(serializer.data)

# who i am view : this view return if current user have admin privilage or not.
@permission_classes([IsAuthenticated])
class WhoIAmView(APIView):
    def get(self , request):
        return(Response({
            "details":request.user.is_superuser
        }))