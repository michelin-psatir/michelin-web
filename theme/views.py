from django.http.response import HttpResponseNotFound, HttpResponseRedirect
from django.shortcuts import render
from django.db import connection
from collections import namedtuple
from .forms import *


def base(request):
    return render(request, 'base.html')