from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.views import generic

from .models import Question, Choice


# def index(request):
#     latest_question_list = Question.objects.all()
#     return render(
#         request,
#         "polls/index.html",
#         {"latest_question_list": latest_question_list},
#     )


# def detail(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(
#         request,
#         "polls/detail.html",
#         {
#             "question": question,
#         },
#     )


# def result(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     return render(
#         request,
#         "polls/results.html",
#         {
#             "question": question,
#         },
#     )


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        return Question.objects.order_by("-publication_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"


class ResultlsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST["choice"])
        selected_choice.votes += 1
        selected_choice.save()
        return redirect("polls:results", question_id)
    except (KeyError, Choice.DoesNotExist):
        return render(
            request,
            "polls/detail.html",
            {
                "question": question,
                "error_message": "Must select a valid option",
            },
        )
