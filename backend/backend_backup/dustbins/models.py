from django.db import models


class Dustbin(models.Model):


    TYPE_CHOICES = (

        ("Organic", "Organic"),

        ("Plastic", "Plastic"),

        ("Paper", "Paper"),

        ("Metal", "Metal"),

        ("E-Waste", "E-Waste"),

        ("General", "General"),

    )


    name = models.CharField(
        max_length=100
    )


    dustbin_type = models.CharField(
        max_length=50,
        choices=TYPE_CHOICES
    )


    latitude = models.DecimalField(
        max_digits=9,
        decimal_places=6
    )


    longitude = models.DecimalField(
        max_digits=9,
        decimal_places=6
    )


    address = models.TextField()


    is_active = models.BooleanField(
        default=True
    )


    is_full = models.BooleanField(
        default=False
    )


    def __str__(self):

        return self.name
    