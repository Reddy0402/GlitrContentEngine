from django.db import models

# Create your models here.
class Jobs(models.Model):


    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("processing", "Processing"),
        ("completed", "Completed"),
    ]
    product_name = models.CharField(max_length=200)
    description = models.TextField()
    reference_image = models.ImageField(
        upload_to="reference_images/",
        null=True,
        blank=True
    )
    generated_prompt = models.TextField(
        blank=True
    )
    generated_image = models.ImageField(
        upload_to="generated_images/",
        null=True,
        blank=True
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return self.product_name
