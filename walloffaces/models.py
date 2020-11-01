import os
from django.db import models
from django.urls import reverse

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
    dob = models.DateField(verbose_name="Date of Birth", blank=True, null=True)
    doc = models.DateField(
        verbose_name="Date of Casualty", blank=True, null=True, help_text="Leave blank if veteran is still living")
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

    def get_remembrances(self):
        remembrances = Remembrance.objects.filter(
            veteran=self.id, approved=True)
        return remembrances

    def remembrance_count(self):
        count = Remembrance.objects.filter(
            veteran=self.id, approved=True).count()
        return count


RELATIONSHIP_CHOICES = [
    ("Husband", "Husband"),
    ("Wife", "Wife"),
    ("Father", "Father"),
    ("Mother", "Mother"),
    ("Son", "Son"),
    ("Daughter", "Daughter"),
    ("Brother", "Brother"),
    ("Sister", "Sister"),
    ("Cousin", "Cousin"),
    ("Served Together", "Served Together"),
    ("College Classmates", "College Classmates"),
    ("Grew Up Together", "Grew Up Together"),
    ("Close Friends", "Close Friends"),
    ("Other", "Other"),
]


class Remembrance(models.Model):
    veteran = models.ForeignKey(
        Veteran, on_delete=models.CASCADE)
    title = models.CharField(max_length=150)
    remembrance = models.TextField()
    name = models.CharField(max_length=100, verbose_name="Your Name")
    email = models.EmailField(verbose_name="Your Email")
    relationship = models.CharField(
        max_length=20, choices=RELATIONSHIP_CHOICES, verbose_name="Relationship to Veteran")
    created_at = models.DateField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.veteran.name + ' - ' + self.title

    def get_absolute_url(self):

        return reverse('vet_detail', kwargs={'pk': self.veteran.pk})
