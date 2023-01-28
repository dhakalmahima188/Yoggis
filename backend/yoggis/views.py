from django.shortcuts import render
from django.http.response import StreamingHttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.conf import settings
from twilio.rest import Client
import schedule
import time
from .models import Yoga, YogaScore, UserDisorder
# from django_crontab import decorators

if settings.SERVE:
    from .posedetection import gen_frames

# @decorators.crontab(minute="30",hour="14")
def sendMessage(request):
    # Twilio account SID and auth token
    account_sid = 'ACb1f5211276b92b89d72bca9b91467ffd'
    auth_token = 'fb5f4197ff6cf48fa678648599a0816d'

    # create a Twilio client
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        to="+9779840044672", 
        from_="+16068067346",
        body='Hello, its a yoga time ! Get fresh and be ready !'
    )
def sendSMS(request):
    schedule.every().day.at("11:50").do(sendMessage)
    while True:
        schedule.run_pending()
        time.sleep(1)

def send_sms_view(request):
    sendSMS(request)
    return render(request, 'yoggis/sendSMS.html')

def videofeed(request):
    if settings.SERVE:
        response = StreamingHttpResponse(gen_frames(), content_type="multipart/x-mixed-replace; boundary=frame")
        response['Cache-Control'] = 'no-cache'
        return response
    return HttpResponseRedirect(reverse('home'))


def yoga(request):
    return render(request, 'yoggis/yoga.html')


def home(request):
    trending_yogas = Yoga.objects.all().exclude(title__in=['Sukasana','Savasana'])
    if len(trending_yogas) >= 4:
        trending_yogas = trending_yogas[0:4]
    unq_ygs = YogaScore.objects.values('yoga').distinct()
    pks = [a['yoga'] for a in unq_ygs]
    ygs = Yoga.objects.filter(pk__in=pks)
    if len(ygs) >= 4:
        ygs = ygs[0:4]
    context = {
        "trending_yogas": trending_yogas,
        "challenges": ygs
    }
    return render(request, 'yoggis/home.html', context)


def general(request):
    general_yogas = Yoga.objects.filter(yoga_category__type__contains="General")
    gen = general_yogas.filter(difficulty__contains="C")
    adv = general_yogas.filter(difficulty__contains="A")
    disorder=gen.filter(avoid_for_disorder__type__contains="Asthma")
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
        leaderboard = YogaScore.objects.filter(yoga__pk__contains=yog.pk).order_by('-score')
        to_avoid = yog.avoid_for_disorder.all()
        context['leaderboard'] = leaderboard
        context['avoid_for'] = to_avoid
        general_yogas = Yoga.objects.filter(yoga_category__type__contains="General")

        gen = general_yogas.filter(difficulty__contains="C")
        disorder=gen.filter(avoid_for_disorder__type__contains="Asthma")
        context['dis']=disorder
    except Yoga.DoesNotExist:
        raise Http404('Book does not exist')

    return render(request, 'yoggis/yoga_detail.html', context=context)
