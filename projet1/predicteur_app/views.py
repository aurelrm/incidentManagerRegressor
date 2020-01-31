
from django.shortcuts import render
from django.http import HttpResponse

from django.http import JsonResponse

from rest_framework.parsers import JSONParser
from rest_framework.renderers import JSONRenderer
import io
import numpy as np

from .models import House

from django.views.decorators.csrf import csrf_exempt


def index(request):
    return HttpResponse('Bienvenue sur mon API de prédiction')

def predict_timedelta(data):
    from sklearn.externals import joblib
    colonnes = ['number', 'reopen_count', 'caller_id', 'opened_by', 'location','category','subcategory','u_symptom','impact','urgency','priority','closed_code','resolved_by','0','1','2','3','4','5','6']
    data   = [[data[colonne] for colonne in colonnes]]
    path_to_model   = "/Users/olivierdupain/Desktop/best_model.sav"
    model           = joblib.load(path_to_model)
    
    timedelta       = model.predict(data)
    #print(data)
    return timedelta

@csrf_exempt
def predict(request):

    if request.method == 'GET':
        return JsonResponse({'Erreur':'Method not allowed'}, status=400)

    elif request.method == 'POST':
        data        = JSONParser().parse(request)
        data["timedelta"] = int(predict_timedelta(data))
        print(data)
        return JsonResponse(data ,status=200)

