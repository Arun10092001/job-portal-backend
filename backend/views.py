from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from django.contrib.auth.models import User

from .models import Job, Applications
from .serializers import RegisterSerializer, JobSerializer, ApplicationSerializer


@api_view(['GET'])
def hello_api(response):
    return Response({"message": "Hello to Django"})


@api_view(['POST'])
def register_user(request):
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered successfully!"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def basic_login(request):
    if request.method == 'GET':
        return Response({
            "message": "Use POST with username and password to log in."
        }, status=status.HTTP_200_OK)

    username = request.data.get('username')
    password = request.data.get('password')

    if not username or not password:
        return Response(
            {"message": "Username and password are required."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    user = authenticate(request, username=username, password=password)
    if user is not None:
        return Response(
            {"user_id": user.id, "username": user.username,
                "message": "Login Successfully"},
            status=status.HTTP_200_OK,
        )

    return Response({"message": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET'])
def jobs_view(request):
    jobs = Job.objects.all()
    serializer = JobSerializer(jobs, many=True)
    return Response(serializer.data)


@api_view(['POST'])
def apply_jobs(request):
    payload = request.data.copy()
    applicant_id = payload.get("applicant") or payload.get("applicants")
    if applicant_id and "applicants" not in payload:
        payload["applicants"] = applicant_id

    if applicant_id and Applications.objects.filter(job_id=payload.get("job"), applicants_id=applicant_id).exists():
        return Response({"message": "You have already applied"}, status=status.HTTP_400_BAD_REQUEST)

    serializer = ApplicationSerializer(data=payload)
    if serializer.is_valid():
        serializer.save()
        return Response({"message": "Application submitted"}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
