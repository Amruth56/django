from django.shortcuts import render
from django.http  import HttpResponse 
from .models import Question
from django.http import Http404
from django.template import loader



def detail(request, question_i):
    try:
        question = Question.objects.get(pk = question_i)
    except Question.DoesNotExist:
        raise Http404("Quotatio does not exist")
    question = {
        'question': question
    }
    return render(request, 'polls/detail.html', question )
        

def results(request, question_id):
    response = "You are looking at results of question %s."
    return HttpResponse(response % question_id)
    
def vote(request, question_id):
    return HttpResponse(f"you are voting on question {question_id}.")


def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:]
    # context to pass data from view to template 
    context = {
        'latest_question_list': latest_question_list
    }
    return render(request, 'polls/index.html', context)

