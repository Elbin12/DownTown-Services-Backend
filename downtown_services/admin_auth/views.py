from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from accounts.models import CustomUser
from worker.models import CustomWorker
from .models import Categories, SubCategories
from .serializer import GetUsers, GetWorkers, GetCategories, SubcategorySerializer
from accounts.views import token_generation_and_set_in_cookie
from worker.models import Services
from worker.serializer import ServiceSerializer
# Create your views here.



class Login(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        print(request.data, 'data')
        user = CustomUser.objects.filter(email = request.data['email']).first()
        if not user:
            return Response({'message': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)
        if not user.is_superuser:
            return Response({'message': 'You are not admin'}, status=status.HTTP_400_BAD_REQUEST)
        if not user.check_password(request.data.get('password')):
            print('kkgj')
            return Response({'message': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)
        response = token_generation_and_set_in_cookie(user)
        
        return response
    

class Users(APIView):
    permission_classes = [permissions.IsAdminUser]
    def get(self, request):
        users = CustomUser.objects.filter(is_superuser=False).order_by('date_joined')
        serailizer = GetUsers(users, many=True)
        return Response(serailizer.data, status=status.HTTP_200_OK)
    

class Block(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        email = request.data.get('email')
        user = CustomUser.objects.filter(email=email).first()
        if user:
            if user.is_active:
                user.is_active = False
            else:
                user.is_active = True
            user.save()
            print(user.is_active, 'lll')
        
        return Response({'isActive':user.is_active}, status=status.HTTP_200_OK)


class Workers(APIView):
    permission_classes = [permissions.IsAdminUser]
    def get(self, request):
        workers = CustomWorker.objects.all().order_by('date_joined')
        serailizer = GetWorkers(workers, many=True)
        return Response(serailizer.data, status=status.HTTP_200_OK)
    

class Requests(APIView):
    permission_classes = [permissions.IsAdminUser]
    def get(self, request):
        workers = CustomWorker.objects.exclude(status='verified').order_by('date_joined')
        print(workers, 'l')
        serailizer = GetWorkers(workers, many=True)
        return Response(serailizer.data, status=status.HTTP_200_OK)

class HandleRequest(APIView):
    permission_classes = [permissions.IsAdminUser]
    def post(self, request):
        status = request.data.get('status')
        user = CustomWorker.objects.filter(email=request.data.get('email')).first()
        if user:
            if status in dict(CustomWorker.STATUS_CHOICES):
                user.status = status
                if status == 'verified':
                    user.is_active = True
                elif status == 'rejected':
                    user.is_active = False
                user.save()
                serializer = GetWorkers(user)
                return Response(serializer.data, status=200)
            else:
                return Response({'error': 'Invalid status'}, status=400)
        return Response({'error': 'User not found'}, status=404)
    
class CategoryManage(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get_object(self, pk):
        try:
            return Categories.objects.get(id=pk)
        except Categories.DoesNotExist:
            return Response(f'category not found on {pk}', status=status.HTTP_404_NOT_FOUND)

    def get(self, request):
        categories = Categories.objects.all()
        serializer = GetCategories(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        print(request.data, 'data')
        serializer = GetCategories(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        print(pk, 'll', request.data)
        category = self.get_object(pk)  
        serializer = GetCategories(category, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        print(request.data, 'ooo')
        category = self.get_object(pk)
        category.delete()
        return Response(status=status.HTTP_200_OK)


class Subcategory(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get_object(self, pk):
        print(pk, 'kk')
        try:
            return SubCategories.objects.get(id=pk)
        except SubCategories.DoesNotExist:
            return Response(f'subcategory not found on {pk}', status=status.HTTP_404_NOT_FOUND)

    def get(self, request):
        sub_categories = SubCategories.objects.all()
        print(sub_categories    )
        serializer = SubcategorySerializer(sub_categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        print(request.data)
        serializer = SubcategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        print(request.data)
        subcategory = self.get_object(pk)
        serializer = SubcategorySerializer(subcategory, request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        print(request.data, 'ooo')
        subcategory = self.get_object(pk)
        subcategory.delete()
        return Response(status=status.HTTP_200_OK)
    
class GetServices(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request):
        services = Services.objects.all()
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)