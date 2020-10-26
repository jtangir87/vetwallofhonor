import os
from django.db import models

from tinymce.models import HTMLField
# Create your models here.
COUNTY_CHOICES = [
    ("Berks", "Berks"),
    ("Bucks", "Bucks"),
    ("Chester", "Chester"),
    ("Delaware", "Delaware"),
    ("Lancaster", "Lancaster"),
    ("Lehigh", "Lehigh"),
    ("Montgomery", "Montgomery"),
    ("Northampton", "Northampton"),
    ("Philadelphia", "Philadelphia"),
]

BRANCH_CHOICES = [
    ("Air Force", "Air Force"),
    ("Army", "Army"),
    ("Marine Corps", "Marine Corps"),
    ("Navy", "Navy"),
    ("Space Force", "Space Force"),
]

STATUS_CHOICES = [
    ("Living", "Living"),
    ("Killed In Action", "Killed In Action"),
    ("Missing In Action", "Missing In Action"),
    ("Remains Recovered", "Remains Recovered"),
    ("Deceased", "Deceased"),
]


def veteran_images(instance, filename):
    upload_path = "veteran_images"
    return os.path.join(upload_path, filename.lower())


class Veteran(models.Model):
    name = models.CharField(max_length=150)
    hometown = models.CharField(max_length=100)
    county = models.CharField(max_length=100, choices=COUNTY_CHOICES)
    dob = models.DateField(verbose_name="Date of Birth")
    doc = models.DateField(
        verbose_name="Date of Casualty", blank=True, null=True)
    branch = models.CharField(
        max_length=150, verbose_name="Branch of Service", choices=BRANCH_CHOICES)
    rank = models.CharField(max_length=50)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES)
    country = models.CharField(
        max_length=100, verbose_name="Country of Service")
    image = models.ImageField(
        upload_to=veteran_images, verbose_name="Headshot")
    bio = models.TextField(verbose_name="Biography")
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name
