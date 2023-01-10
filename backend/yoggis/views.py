
from django.shortcuts import render
 
# import view sets from the REST framework
from rest_framework import viewsets
 
# import the TodoSerializer from the serializer file
from .serializers import YogaSerializer
 
# import the Todo model from the models file
from .models import Yoga
from django.http import HttpResponse
import cv2
import math
from time import time
# import mediapipe as mp
# import matplotlib.pyplot as plt
import statistics
import numpy as np
 
# create a class for the Todo model viewsets
class YogaView(viewsets.ModelViewSet):
 
    # create a serializer class and
    # assign it to the TodoSerializer class
    serializer_class = YogaSerializer
 
    # define a variable and populate it
    # with the Todo list objects
    queryset = Yoga.objects.all()