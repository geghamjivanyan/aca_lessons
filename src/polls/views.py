import random 
import string

from django.shortcuts import get_object_or_404, render
from django.http import Http404

from .models import Question, Choice, PollUser, ApiKey
# Create your views here.
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse


def index(request):
    username = request.GET.get('username', '')
    api_key = request.GET.get('api_key', '')
    
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = None

    if user:
        apk = ApiKey.objects.get(username=username)
        if apk.api_key == api_key:
            lq = Question.objects.order_by("-pub_date")[:5]
            context = {"latest_question_list": lq}

            context["user_info"] = user.first_name 
            return render(request, "polls/index.html", context)
    else:
        return HttpResponse("Authentication credentials missed or not valid")

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})


def vote(request, question_id):

    username = request.GET['username']
    api_key = request.GET['api_key']

    user = User.objects.get(username=username)
    if user:
        apk = ApiKey.objects.get(username=username)
        if apk.api_key == api_key:

            question = get_object_or_404(Question, pk=question_id)
            try:
                print("CHoice id - ", request.POST["choice"])
                selected_choice = question.choice_set.get(pk=request.POST["choice"])
            except (KeyError, Choice.DoesNotExist):
                # Redisplay the question voting form.
                return render(
                    request,
                    "polls/detail.html",
                    {
                        "question": question,
                        "error_message": "You didn't select a choice.",
                    },
                )
            else:
                print("S - ", selected_choice.votes)
                selected_choice.votes += 1
                selected_choice.save()
                print("E - ", selected_choice.votes)
                # Always return an HttpResponseRedirect after successfully dealing
                # with POST data. This prevents data from being posted twice if a
                # user hits the Back button.
                return HttpResponseRedirect(reverse("polls:results", args=(question.id,)))



def login(request):
    if request.method == 'GET':
        return render(request, "polls/login.html")
    else:
        username = request.POST["username"]
        password = request.POST["password"]

        print(username, password)

        user = authenticate(username=username, password=password)

        if user:
            apk = ApiKey.objects.get(username=username)
            return HttpResponseRedirect("/polls/?username={}&api_key={}".format(username, apk.api_key)) # send apk.api_key
        else:
            return render(request, "polls/login.html", context={"error": "wrong login or password"})

def register(request):
    if request.method == 'GET':
        return render(request, "polls/register.html")

    else:
        username = request.POST["username"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        password = request.POST['password']
        
        user = User.objects.create_user(username=username, password=password)
        user.first_name=firstname
        user.last_name=lastname
        user.save()

        PollUser(user=user).save()
        letters = string.ascii_lowercase
        ApiKey(username=user.username, api_key=''.join(random.choice(letters) for i in range(16))).save()
        return HttpResponseRedirect("/polls/login")
    

def log_out(request):
    logout(request)
    return HttpResponseRedirect("/polls/login")
