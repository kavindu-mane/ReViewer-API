from rest_framework.views import APIView
from django.db.models import Q , Count
from . models import User , Book , Review
from . serializers_admin import  BookSerializer
from . serializers import AccountSerializer
from django.core.paginator import Paginator
from rest_framework.response import Response
from rest_framework.exceptions import PermissionDenied
from rest_framework.decorators import  permission_classes , parser_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser , FormParser
from django.db.models.functions import TruncDay
from django.utils import timezone
from django.utils.timezone import timedelta

# get users view : this view return users with paginations
# only accessible for admin
# serializer : AccountSerializer in serializers.py
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
            serializer = AccountSerializer(paginated_users , many = True)
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

# get books view : this view return books with paginations
# only accessible for admin
# serializer : BookSerializer in serializers.py
@permission_classes([IsAuthenticated])
class getBooks(APIView):
    def post(self,request):
        if request.user.is_superuser:
            page = request.data["page"]
            search = None;
            if "search" not in request.data or request.data["search"] == "":
                books = Book.objects.order_by("title")
            else:
                search = request.data["search"]
                books = Book.objects.filter(Q(title__icontains=search) | Q(author__icontains=search) | Q(isbn__icontains=search)).order_by("title")

            paginator = Paginator(books, 10)
            paginated_books = paginator.get_page(page)
            serializer = BookSerializer(paginated_books , many = True)

            return Response({"books":serializer.data , 
                            "meta":{
                                "count":paginator.count , 
                                "page_count":paginator.num_pages,
                                "start":paginated_books.start_index(),
                                "end":paginated_books.end_index()
                                }
                            })
        else:
            raise PermissionDenied({"details":"You don't have permission to this action."})


# chnage user status : admin can user account activate or deactivate through this
# only accessible for admin
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

# add new book view : admin can add new book with this view.
# only accessible for admin
# it will return success , error or raise PermissionDenied exception
# serializer : BookSerializer in serializers_admin.py
@permission_classes([IsAuthenticated])
@parser_classes([MultiPartParser , FormParser])
class addNewBook(APIView):
    def post(self,request):
        if request.user.is_superuser:
            try:
                isbn = request.data["isbn"]
                book = Book.objects.filter(isbn=isbn).first()

                # check isbn already exist or not
                if book is not None:
                    return Response({
                    "isbn" : "This isbn already registered"
                })
                serializer = BookSerializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response({
                    "details" : "success"
                })
            except KeyError:
                return Response({
                    "details":"error"
                })
        else:
            raise PermissionDenied({"details":"You don't have permission to this action."})

# get admin stats : this view return admin stats for dashboard    
@permission_classes([IsAuthenticated])
class GetAdminStats(APIView):
    def get(self , request , type):
        try:
            time  = timezone.now().date() - timedelta(days=7)           
            time_old  = timezone.now().date() - timedelta(days=14)
            model = Book
            if type == "users": 
                model = User
            elif type == "reviews":
                model = Review

            if request.user.is_superuser:
                # books new
                books = model.objects.filter(created_at__gte=time
                ).annotate(
                    day=TruncDay('created_at__date'),
                    created_count=Count('created_at__date')
                ).values(
                    'day',
                ).annotate(
                    created_count=Count('created_at__date')
                ).order_by('day')

                books = list(books)

                for i in range(7):
                    new_date = time + timedelta(days=i + 1)
                    result_list = [d["day"] for d in books]
                    if new_date not in result_list:
                        books.append({'day': new_date, 'created_count': 0})
                books = sorted(books, key=lambda x: x['day'])
                

                # books old
                books_old = model.objects.filter(created_at__gte=time_old,
                                                created_at__lte=time
                ).annotate(
                    day=TruncDay('created_at__date'),
                    created_count=Count('created_at__date')
                ).values(
                    'day',
                ).annotate(
                    created_count=Count('created_at__date')
                ).order_by('day')

                books_old = list(books_old)

                for i in range(7):
                    new_date = time_old + timedelta(days=i+1)
                    result_list = [d["day"] for d in books_old]
                    if new_date not in result_list:
                        books_old.append({'day': new_date, 'created_count': 0})
                books_old = sorted(books_old, key=lambda x: x['day'])
                return Response({
                    "new":books,
                    "old":books_old
                })
            else:
                return Response({
                    "new":[],
                    "old":[]
                })
        except:
            return Response({"details":"error"})