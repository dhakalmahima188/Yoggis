
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
    response= StreamingHttpResponse(gen_frames(), content_type="multipart/x-mixed-replace; boundary=frame")
    response['Cache-Control'] = 'no-cache'
    return response

def yoga(request):
    return render(request,'yoggis/yoga.html')

def home(request):
    return render(request,'yoggis/home.html')

def general(request):
    return render(request,'yoggis/general.html')

def challenges(request):
    return render(request,'yoggis/challenges.html')

def chronic(request):
    return render(request,'yoggis/chronic.html')