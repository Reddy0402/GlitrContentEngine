from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status

# For quick local testing of the API POST from browser/front-end without CSRF token
from django.views.decorators.csrf import csrf_exempt

from .models import Jobs
from .Serializers import JobSerializer
import logging

logger = logging.getLogger(__name__)

def index(request):
    """Render the main frontend page"""
    return render(request, 'index.html')

@api_view(["GET"])
def health_check(request):
    return Response(
        {
            "status": "healthy"
        }
    )
@csrf_exempt
@api_view(["POST"])
def generate_job(request):
    logger.info("generate_job called: method=%s, path=%s", request.method, request.path)
    # Log CSRF-related headers and cookies for debugging
    try:
        csrf_header = request.META.get('HTTP_X_CSRFTOKEN')
        cookie_header = request.META.get('HTTP_COOKIE')
        logger.info("CSRF header: %s", csrf_header)
        logger.info("Cookie header: %s", cookie_header)
    except Exception:
        logger.exception("Error reading request META for CSRF debug")

    data = request.data.copy()
    if 'product_description' in data:
        data['description'] = data['product_description']
    if 'product_image' in data:
        data['reference_image'] = data['product_image']

    serializer = JobSerializer(data=data)

    if serializer.is_valid():

        job = serializer.save()
        
        # Update Status = Processing
        job.status = "processing"
        job.save()

        try:
            from jobs.services.grok_service import generate_prompt, generate_mock_image
            # Call generate_prompt()
            prompt = generate_prompt(job.product_name, job.description)
            job.generated_prompt = prompt
            
            # Mock image generation
            image_url = generate_mock_image(prompt)
            
            # Download the mock image and save it to the ImageField
            import requests as req
            from django.core.files.base import ContentFile
            img_response = req.get(image_url, timeout=10)
            if img_response.status_code == 200:
                job.generated_image.save(f"mock_{job.id}.png", ContentFile(img_response.content), save=False)
            
            # Update Status = Completed
            job.status = "completed"
            job.save()
        except Exception as e:
            # If Grok fails, Update Status = Failed
            job.status = "failed"
            # The model does not contain an error field, so we just store the status
            job.save()

        # Return Job
        return Response(
            JobSerializer(job).data,
            status=status.HTTP_201_CREATED
        )

    return Response(
        serializer.errors,
        status=status.HTTP_400_BAD_REQUEST
    )

@api_view(["GET"])
def job_detail(request, job_id):

    try:

        job = Jobs.objects.get(id=job_id)

    except Jobs.DoesNotExist:

        return Response(
            {
                "error": "Job not found"
            },
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = JobSerializer(job)
    data = serializer.data
    
    # The frontend app.js expects capitalized statuses: 'Completed', 'Failed', 'Processing'
    if data.get('status') == 'completed':
        data['status'] = 'Completed'
    elif data.get('status') == 'failed':
        data['status'] = 'Failed'
    elif data.get('status') == 'processing':
        data['status'] = 'Processing'
        
    # The frontend expects 'prompt' and 'image_url' instead of 'generated_prompt' and 'generated_image'
    data['prompt'] = data.get('generated_prompt')
    
    if data.get('status') == 'Completed' and data.get('prompt'):
        from jobs.services.grok_service import generate_mock_image
        data['image_url'] = generate_mock_image(data['prompt'])
    else:
        data['image_url'] = data.get('generated_image')

    return Response(data)