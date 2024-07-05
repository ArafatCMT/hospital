from django.db import models
from django.contrib.auth.models import User
from patient.models import Patient
from .constants import STAR_CHOICES
# Create your models here.
class Designation(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField()

    def __str__(self):
        return self.name


class Specialization(models.Model):
    name = models.CharField(max_length=30)
    slug = models.SlugField()

    def __str__(self):
        return self.name

class AvailableTime(models.Model):
    time = models.CharField(max_length=30)

    def __str__(self):
        return self.time

class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='doctor/images/')
    designation = models.ManyToManyField(Designation)
    specialization = models.ManyToManyField(Specialization)
    available_time = models.ManyToManyField(AvailableTime)
    fee = models.IntegerField()
    meet_link = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"


class Review(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    body = models.TextField()
    created = models.DateField(auto_now_add=True)
    rating = models.CharField(choices=STAR_CHOICES, max_length=15)

    def __str__(self):
        return f"Patient: {self.patient.user.first_name} , Doctor: {self.doctor.user.first_name}"