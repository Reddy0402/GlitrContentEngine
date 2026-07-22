from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

from .models import Job
from .serializers import JobSerializer

@api_view(["GET"])
def health_check(request):
    return Response(
        {
            "status": "healthy"
        }
    )
@api_view(["POST"])
def generate_job(request):

    serializer = JobSerializer(data=request.data)

    if serializer.is_valid():

        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(["GET"])
def job_detail(request, job_id):

    try:

        job = Job.objects.get(id=job_id)

    except Job.DoesNotExist:

        return Response(
            {
                "error": "Job not found"
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = JobSerializer(job)

    return Response(serializer.data)