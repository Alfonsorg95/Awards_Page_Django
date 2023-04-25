from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello World")


def detail(request, question_id):
    return HttpResponse(f"Question number: {question_id}")


def result(request, question_id):
    return HttpResponse(f"Results of question number: {question_id}")


def vote(request, question_id):
    return HttpResponse(f"Voting to question number: {question_id}")
