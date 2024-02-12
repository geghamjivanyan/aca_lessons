from django.shortcuts import get_object_or_404, render
from django.http import Http404

from .models import Question, Choice
# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse


def index(request):
    lq = Question.objects.order_by("-pub_date")[:5]
    context = {"latest_question_list": lq}
    return render(request, "polls/index.html", context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/detail.html", {"question": question})


def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, "polls/results.html", {"question": question})


def vote(request, question_id):
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
