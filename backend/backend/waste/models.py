from django.db import models
from django.conf import settings


class WasteScan(models.Model):
    WASTE_TYPES = [
        ("Plastic", "Plastic"),
        ("Paper", "Paper"),
        ("Glass", "Glass"),
        ("Metal", "Metal"),
        ("Organic", "Organic"),
        ("E-Waste", "E-Waste"),
        ("Unknown", "Unknown"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="waste_scans"
    )

    image = models.ImageField(upload_to="waste_images/")

    waste_type = models.CharField(
        max_length=50,
        choices=WASTE_TYPES,
        default="Unknown"
    )

    confidence_score = models.FloatField(default=0.0)

    recommendation = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.waste_type}"