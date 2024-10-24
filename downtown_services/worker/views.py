from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status
from accounts.models import CustomUser
from .models import CustomWorker, WorkerProfile, Services
from .serializer import WorkerRegisterSerializer, WorkerLoginSerializer, ServiceSerializer

import jwt, datetime
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from .serializer import WorkerDetailSerializer
from admin_auth.serializer import GetCategories
from admin_auth.models import Categories

from rest_framework.parsers import MultiPartParser, FormParser

from accounts.utils import upload_fileobj_to_s3
import time
import os
from datetime import datetime
# Create your views here.


class CheckingCredentials(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        print(request.data)
        email = request.data.get('email')
        mob = request.data.get('mob')
        if CustomWorker.objects.filter(email=email).exists():
            return Response({'message':'An account is already registered with this email'}, status=status.HTTP_400_BAD_REQUEST)
        if CustomWorker.objects.filter(mob=mob).exists():
            return Response({'message':'An account is already registered with this mobile number'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = GetCategories(Categories.objects.all(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SignUp(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = WorkerRegisterSerializer(data=request.data)
        if serializer.is_valid():
            print('llll')
            serializer.save()
        else:
            print(serializer.errors, 'err')
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        print(serializer, serializer.data)

        return Response(serializer.data, status=status.HTTP_200_OK)


class Login(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        print('hi', request.data)
        if not request.data.get('email'):
            return Response({'message': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST) 
        worker = CustomWorker.objects.filter(email = request.data['email']).first()
        print(worker, 'gkg')
        if not worker:
            return Response({'message': 'Invalid email'}, status=status.HTTP_400_BAD_REQUEST)
        
        if not worker.check_password(request.data.get('password')):
            return Response({'message': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)
        
        if worker.status=='rejected':
            return Response({'message': 'You are rejected by admin'}, status=status.HTTP_400_BAD_REQUEST)
        if worker.status == 'in_review':
            return Response({'message': 'Your request are in progress.'}, status=status.HTTP_400_BAD_REQUEST)
        
        worker_profile = WorkerProfile.objects.filter(user=worker).first()

        refresh = RefreshToken()
        refresh['worker_id'] = str(worker.id)
        refresh['user_type'] = 'worker'
        refresh["email"] = str(worker.email)
        content = {
            'isActive': worker.is_active,
            'isAdmin' : worker.is_superuser,
            'isWorker': worker.is_staff,
            'email':worker.email,
            'mob':worker.mob
        }

        if worker_profile:
            serializer = WorkerDetailSerializer(worker)
            content.update(serializer.data)

        response = Response(content, status=status.HTTP_200_OK)
        response.set_cookie(
                key = 'worker_access_token',
                value = str(refresh.access_token),
                secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
                httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
                samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
            )
        response.set_cookie(
            key = 'worker_refresh_token',
            value = str(refresh),
            secure = settings.SIMPLE_JWT['AUTH_COOKIE_SECURE'],
            httponly = settings.SIMPLE_JWT['AUTH_COOKIE_HTTP_ONLY'],
            samesite = settings.SIMPLE_JWT['AUTH_COOKIE_SAMESITE']
        )
        
        return response
    
class Profile(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        worker = CustomWorker.objects.get(user=request.user)
        serializer = WorkerDetailSerializer(worker)
        if serializer.is_valid():
            return Response(serializer.data,status=status.HTTP_200_OK)
        return Response(serializer.errors,status=status.HTTP_200_OK)
    
    def put(self, request):
        worker = request.user
        serializer = WorkerDetailSerializer(worker, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def post(self, request):
        print(request.user, 'lggk', request.data, request.user, request.user.id)
        print(request.FILES, 'kkk')
        serializer = WorkerDetailSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():    
            print('hiiii')
            worker_profile, created = WorkerProfile.objects.get_or_create(user=request.user)
            worker_profile.first_name = request.data.get('first_name', worker_profile.first_name)
            worker_profile.last_name = request.data.get('last_name', worker_profile.last_name)
            worker_profile.dob = request.data.get('dob', worker_profile.dob)
            worker_profile.gender = request.data.get('gender', worker_profile.gender)
            request.user.mob = request.data.get('mob')
            if 'profile_pic' in request.FILES:
                print(request.FILES, 'llll')
                file = request.FILES['profile_pic']
                file_extension = os.path.splitext(file.name)[1]
                current_time_str = datetime.now().strftime("%Y%m%d_%H%M%S")
                unique_filename = f"{current_time_str}{file_extension}"
                s3_file_path = f"workers/profile_pic/{unique_filename}"
                try:
                    image_url = upload_fileobj_to_s3(file, s3_file_path)
                    if image_url:
                        worker_profile.profile_pic = s3_file_path
                        print("Image URL:", image_url)
                    else:
                        return Response({'error': 'File upload failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                except Exception as e:
                    print(e)
                    return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                print(worker_profile.profile_pic)

            worker_profile.save()
            request.user.save()

            serializer = WorkerDetailSerializer(request.user)
        
        else:
            return Response(serializer.errors, status=status.HTTP_422_UNPROCESSABLE_ENTITY)

        return Response(serializer.data, status=status.HTTP_200_OK)
    

class Logout(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request):
        try:
            refresh_token = request.COOKIES.get("worker_refresh_token")
            token = RefreshToken(refresh_token)
            token.blacklist()
            response = Response(status=status.HTTP_205_RESET_CONTENT)
            response.delete_cookie('worker_refresh_token')
            response.delete_cookie('worker_access_token')
            response.delete_cookie('csrftoken')
            return response
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

class ServicesManage(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)

    def get_object(self, pk):
        print(pk, 'kk')
        try:
            return Services.objects.get(id=pk)
        except Services.DoesNotExist:
            return Response(f'subcategory not found on {pk}', status=status.HTTP_404_NOT_FOUND)

    def get(self, request):
        services = Services.objects.filter(worker=request.user)
        serializer = ServiceSerializer(services, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        print(request.data, 'data')
        serializer = ServiceSerializer(data=request.data,  context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, pk):
        print(request.data)
        subcategory = self.get_object(pk)
        serializer = ServiceSerializer(subcategory, request.data, context={'request': request}, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)