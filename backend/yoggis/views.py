from django.shortcuts import render
from django.http.response import StreamingHttpResponse, HttpResponseRedirect, Http404
from django.urls import reverse
from django.conf import settings

from .models import Yoga, YogaScore, UserDisorder
# from django_crontab import decorators
from django.contrib.auth.models import User, auth
from django.shortcuts import redirect
from django.contrib import messages
from .models import Yoga, YogaScore, UserDisorder, SUserDisorder
from django.contrib.auth.decorators import login_required

if settings.SERVE:
    from .posedetection import gen_frames
    from .newposedetection import genFrames


def videofeed(request):
    if settings.SERVE:
        response = StreamingHttpResponse(genFrames(True), content_type="multipart/x-mixed-replace; boundary=frame")
        response['Cache-Control'] = 'no-cache'
        return response
    return HttpResponseRedirect(reverse('home'))


def yoga(request):
    return render(request, 'yoggis/yoga.html')

@login_required(login_url='/login')
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

@login_required(login_url='/login')
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

@login_required(login_url='/login')
def chronic(request):
    yogas = Yoga.objects.all()
    asthmaa = yogas.filter(yoga_category__type__contains="Asthma")
    back = yogas.filter(yoga_category__type__contains="Back-Pain")
    context = {
        "asthma": asthmaa,
        "backpain": back
    }
    return render(request, 'yoggis/chronic.html', context)

@login_required(login_url='/login')
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
@login_required(login_url='/login')
def yoga_detail_view(request, pk1):
    context = {}
    try:
        yog = Yoga.objects.get(pk=pk1)
        yog
        context['yoga'] = yog
        leaderboard = YogaScore.objects.filter(yoga__pk__contains=yog.pk).order_by('-score')
        to_avoid = yog.avoid_for_disorder.all()
        context['leaderboard'] = leaderboard
        context['avoid_for'] = to_avoid
        general_yogas = Yoga.objects.filter(yoga_category__type__contains="General")
        backpain_yogas = Yoga.objects.filter(yoga_category__type__contains="Back-Pain")
        gen = general_yogas.filter(difficulty__contains="C")
        context['gen']=gen
        context['backpain']=backpain_yogas
        disorder=gen.filter(avoid_for_disorder__type__contains="Asthma")
        context['dis']=disorder
        context['category']=yog.yoga_category.all()
        
    except Yoga.DoesNotExist:
        raise Http404('Book does not exist')

    return render(request, 'yoggis/yoga_detail.html', context=context)




#Login and Register
def login(request):
    if request.method== 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            messages.info(request,'invalid credentials')
            return redirect('login')

    else:
        return render(request,'yoggis/login.html')    

def register(request):

    if request.method == 'POST':
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        email = request.POST['email']

        if password1==password2:
            if User.objects.filter(username=username).exists():
                messages.info(request,'Username Taken')
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,'Email Taken')
                return redirect('register')
            else:   
                user = User.objects.create_user(username=username, password=password1, email=email,first_name=first_name,last_name=last_name)
                user.save();
                print('user created')
                return redirect('login')

        else:
            messages.info(request,'password not matching..')    
            return redirect('yoggis/register')
        return redirect('/')
        
    else:
        return render(request,'yoggis/register.html')



def logout(request):
    auth.logout(request)
    return redirect('yoggis/login.html')       

@login_required(login_url='/login')
def profile(request):
    disorders = UserDisorder.objects.all()
    s_disorders=SUserDisorder.objects.filter(user=request.user)
   
    s_disord={
        "s_name": s_disorders,
         "name": disorders
    }
    
  
    return render(request, 'yoggis/profile.html', s_disord)
    # return render(request,'yoggis/profile.html')
    
def updateUserDisorder(request,pid):
    try:
        print("hello",pid)
        d_obj = UserDisorder.objects.get(pk=pid)
        print(d_obj)
        print(request.user)
        sd_obj = SUserDisorder.objects.get(user=request.user)
        print(sd_obj)
        if sd_obj:
            print("existing object")
            sd_obj.user_disorder.add(d_obj)
        else:
            print("hello making new object")
            SUserDisorder.objects.create(user=request.user.id, user_disorder=d_obj.id)
    except:
        pass 
    return redirect('profile')
    
# def updateUserDisorder(request, pid):
#     try:
#         print("hello", pid)
#         d_obj = UserDisorder.objects.get(pk=pid)
#         print(d_obj)
#         print(request.user)
#         sd_obj, created = SUserDisorder.objects.get(user=request.user)
#         if not created:
#             sd_obj.user_disorder.add(d_obj)
#         else:
#             sd_obj.user_disorder.set([d_obj])
#     except Exception as e:
#         print(e)
    
#     return("profile")
   