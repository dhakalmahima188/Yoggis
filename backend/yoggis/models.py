from django.db import models
from django.contrib.auth.models import User



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
    BEGINNER = 'C'
    INTERMEDIATE = 'B'
    ADVANCEDINTERMEDIATE = 'A'
    EXPERT = 'S'
    DIFFICULTY_CHOICES = [
        (BEGINNER, 'Beginner'),
        (INTERMEDIATE, 'Intermediate'),
        (ADVANCEDINTERMEDIATE, 'Advanced Intermediate'),
        (EXPERT, 'Expert')
    ]

    title = models.CharField(max_length=50)
    description = models.TextField()
    how_to_perform = models.TextField(blank=True)
    image = models.ImageField(upload_to='yogaImages/')
    # age group
    lower_age = models.IntegerField(default=0)
    upper_age = models.IntegerField(default=0)
    difficulty = models.CharField(
        max_length=1,
        choices=DIFFICULTY_CHOICES,
        default=BEGINNER,
    )
    yoga_category = models.ManyToManyField(YogaCategory)
    avoid_for_disorder = models.ManyToManyField(UserDisorder, blank=True)

    def __str__(self):
        return self.title


class CorrectVectorLocations(models.Model):
    angle_location = models.CharField(max_length=20)
    angle_value = models.FloatField()
    angle_of = models.ForeignKey(Yoga, on_delete=models.CASCADE)

    def __str__(self):
        return self.angle_location


class YogaScore(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    yoga = models.ForeignKey(Yoga, on_delete=models.CASCADE, related_name='yogaOwner')

    def __str__(self):
        return self.user.username
    
class SUserDisorder(models.Model):
       user_disorder=models.ManyToManyField(UserDisorder,blank=True)
       user=models.ForeignKey(User,on_delete=models.CASCADE)