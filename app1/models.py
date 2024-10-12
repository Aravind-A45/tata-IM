from django.db import models
from django.contrib.auth.models import Group, User, auth

# Create your models here.
class File(models.Model):
    file = models.FileField(upload_to = 'uploads')

class Components(models.Model):
    material_no = models.CharField(max_length=255)
    material_name = models.CharField(max_length=255)
    movement_type = models.PositiveIntegerField()
    centre = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    unit_of_entry = models.CharField(max_length=255)
    plant_no = models.CharField(max_length=255)
    receiving_storage_location = models.CharField(max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
      return self.material_name    