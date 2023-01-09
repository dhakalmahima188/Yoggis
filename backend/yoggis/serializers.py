
# import serializers from the REST framework
from rest_framework import serializers
 
# import the todo data model
from .models import Yoga
 
# create a serializer class
class YogaSerializer(serializers.ModelSerializer):
    # specify the model to be used
    class Meta:
        model = Yoga
        # specify the fields to be used
        fields = ('id',
                  'title',
                  'description',
                  'image')