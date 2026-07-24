This project is a Django-based backend application with a simple HTML, CSS, and JavaScript frontend for generating AI-powered content jobs. 
The backend exposes REST APIs to create and manage generation requests, while the frontend provides a lightweight interface for users to submit prompts and view the generated results.

Project Structure

The project is organized into the following main components:

manage.py – Entry point for running Django management commands.
config/ – Contains the project's settings and URL configuration (settings.py and urls.py).
myapp/ – Main application responsible for models, serializers, views, and API endpoints.
jobs/services/grok_service.py – Handles communication with the Grok service used for content generation.
Backend

The backend follows Django REST Framework conventions.

models.py defines the Jobs model, which stores information about each content generation request, including its status and generated output.
admin.py registers the Jobs model so it can be managed through the Django Admin panel.
Serializers.py contains the JobSerializer, which converts model instances to and from JSON for the REST APIs.
views.py implements the API endpoints responsible for creating jobs, retrieving job status, and performing health checks.
urls.py maps the application's API routes, including:
/api/generate/ – Creates a new content generation job.
/api/jobs/<id>/ – Returns the current status and results of a specific job.
/api/health/ – Provides a simple health check endpoint.
Frontend

The frontend is intentionally kept simple and is rendered using Django templates instead of a separate React or Vue application.

templates/index.html serves as the main user interface.
static/js/app.js manages form submission, API requests, and periodically checks the job status.
static/css/style.css contains the styling for the webpage.
Application Workflow

The application follows a straightforward request-response workflow:

The user opens the home page (/) and submits a content generation request.
The frontend sends the request to the /api/generate/ endpoint.
The backend creates a new Jobs record with its initial status set to processing.
The backend invokes grok_service.generate_prompt() to generate the text content and generate_mock_image() to create a sample image.
Once processing finishes, the job status is updated to either completed or failed.
Meanwhile, the frontend continuously polls /api/jobs/<id>/ until the job is complete and then displays the generated content.
Current Issues

The project currently encounters a compatibility issue between Python 3.14 and Django 4.2.30.

During template rendering in the Django Admin interface, an exception is raised inside django.template.context.Context.__copy__. The error occurs because super().__copy__() attempts to access a dicts attribute that is not available in the parent object. This appears to be caused by running a Django version that does not yet fully support Python 3.14.

Additional Observations

A few implementation details are worth noting:

The JobSerializer marks updated_at as a read-only field, but the Jobs model does not currently define an updated_at attribute. This inconsistency should be corrected to avoid serializer errors.
The image generation process currently uses a placeholder implementation by downloading images from Pollinations AI through generate_mock_image(). A production-ready image generation service can later replace this mock implementation.
The project is configured to use PostgreSQL as its database, with the connection details provided through environment variables, making it easy to configure different environments without modifying the source code.
