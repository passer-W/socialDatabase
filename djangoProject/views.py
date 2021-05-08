from django.shortcuts import render
import datetime


def runoob(request):
    context = {}
    context['title'] = "test"
    context['hello'] = 'Hello World!'
    context["now"] = datetime.datetime.now()
    return render(request, 'test.html', context)
