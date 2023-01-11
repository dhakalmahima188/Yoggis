
from django.shortcuts import render
from django.http.response import StreamingHttpResponse
 
# import view sets from the REST framework
from rest_framework import viewsets
 
# import the TodoSerializer from the serializer file
from .serializers import YogaSerializer
 
# import the Todo model from the models file
from .models import Yoga
from .posedetection import gen_frames

# create a class for the Todo model viewsets
class YogaView(viewsets.ModelViewSet):
 
    # create a serializer class and
    # assign it to the TodoSerializer class
    serializer_class = YogaSerializer
 
    # define a variable and populate it
    # with the Todo list objects
    queryset = Yoga.objects.all()

#put below code in a class to render somewhere
def videofeed(request):
    return StreamingHttpResponse(gen_frames(), content_type="image/jpeg")

def yoga(request):
    return render(request,'yoggis/yoga.html')