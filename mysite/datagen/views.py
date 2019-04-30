from django.shortcuts import render, get_object_or_404

# Create your views here.

from django.http import HttpResponse

from .models import *

def index(request):
    experiment_list = Experiment.objects.all()
    context = {'experiment_list': experiment_list}
    return render(request, 'datagen/index.html', context)

def experiment(request, experiment_id):
    exp = get_object_or_404(Experiment, pk=experiment_id)
    return render(request, 'datagen/experiment.html', {'experiment': exp})