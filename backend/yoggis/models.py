from django.db import models

# Create your models here.

class Yoga(models.Model):
    
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to='yoga_images/')

    def __str__(self):
        return self.title
