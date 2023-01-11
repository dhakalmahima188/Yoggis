from django.db import models


class UserDisorder(models.Model):
    type = models.CharField(max_length=40)
    description = models.TextField()
    user_disorder_image = models.ImageField(upload_to='userDisorderImages/')

    def __str__(self):
        return self.type


class YogaCategory(models.Model):
    type = models.CharField(max_length=40)
    description = models.TextField()
    category_image = models.ImageField(upload_to='yogaCategoryImages/')

    def __str__(self):
        return self.type


class Yoga(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    image = models.ImageField(upload_to='yogaImages/')
    # age group
    lower_age = models.IntegerField(default=0)
    upper_age = models.IntegerField(default=0)
    yoga_category = models.ManyToManyField(YogaCategory)
    avoid_for_disorder = models.ManyToManyField(UserDisorder)

    def __str__(self):
        return self.title


class CorrectVectorLocations(models.Model):
    angle_location = models.CharField()
    angle_value = models.FloatField()
    angle_of = models.ForeignKey(Yoga, on_delete=models.CASCADE)
