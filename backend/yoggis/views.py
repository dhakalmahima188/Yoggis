from django.shortcuts import render
from django.http.response import StreamingHttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.conf import settings


from .models import Yoga, YogaScore, UserDisorder


if settings.SERVE:
    from .posedetection import gen_frames


def videofeed(request):
    if settings.SERVE:
        response = StreamingHttpResponse(gen_frames(), content_type="multipart/x-mixed-replace; boundary=frame")
        response['Cache-Control'] = 'no-cache'
        return response
    return HttpResponseRedirect(reverse('home'))


def yoga(request):
    return render(request, 'yoggis/yoga.html')


def home(request):
    trending_yogas = Yoga.objects.all()
    if len(trending_yogas) >= 4:
        trending_yogas = trending_yogas[0:4]
    leaderboard = YogaScore.objects.all()
    if len(leaderboard) >= 5:
        leaderboard = leaderboard[0:5]
    context = {
        "trending_yogas": trending_yogas,
        "leaderboard": leaderboard
    }
    return render(request, 'yoggis/home.html', context)


def general(request):
    general_yogas = Yoga.objects.filter(yoga_category__type__contains="General")
    gen = general_yogas.filter(difficulty__contains="C")
    adv = general_yogas.filter(difficulty__contains="A")
    print("gen")
    context = {
        "general": gen,
        "advanced": adv
    }
    return render(request, 'yoggis/general.html', context)


def chronic(request):
    yogas = Yoga.objects.all()
    asthmaa = yogas.filter(yoga_category__type__contains="Asthma")
    back = yogas.filter(yoga_category__type__contains="Back-Pain")
    context = {
        "asthma": asthmaa,
        "backpain": back
    }
    return render(request, 'yoggis/chronic.html', context)

def meditation(request):
    med=Yoga.objects.filter(yoga_category__type__contains="Meditation")
    context={
        "meditation":med
    }
    return render(request,'yoggis/meditation.html',context)
    


def challenges(request):
    
    
    return render(request, 'yoggis/challenges.html')


def squad(request):
    return render(request, 'yoggis/squad.html')


# def challenges(request):
#     return render(request,'yoggis/challenges.html')

def session(request):
    return render(request, 'yoggis/session.html')


def tpose(request):
 
    return render(request, 'yoggis/tpose.html')


# def leaderboard(request):
#     return render(request,'yoggis/leaderboard.html')

def yoga_detail_view(request, pk1):
    context = {}
    try:
        yog = Yoga.objects.get(pk=pk1)
        context['yoga'] = yog
        leaderboard = YogaScore.objects.filter(yoga__pk__contains=yog.pk)
        to_avoid = yog.avoid_for_disorder.all()
        context['leaderboard'] = leaderboard
        context['avoid_for'] = to_avoid
    except Yoga.DoesNotExist:
        raise Http404('Book does not exist')

    return render(request, 'yoggis/yoga_detail.html', context=context)
