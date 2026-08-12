from django.db import models
from django.conf import settings


class Complaint(models.Model):

    STATUS_CHOICES = [

        ("PENDING", "Pending"),

        ("PROCESSING", "Processing"),

        ("RESOLVED", "Resolved"),

    ]


    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="complaints"
    )


    title = models.CharField(
        max_length=200
    )


    description = models.TextField()


    location = models.CharField(
        max_length=255,
        blank=True
    )


    image = models.ImageField(
        upload_to="complaints/",
        blank=True,
        null=True
    )


    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )



    def __str__(self):

        return self.title