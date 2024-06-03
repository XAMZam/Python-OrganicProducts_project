from django.shortcuts import render
from django.http import HttpResponse
from .models import Shampoo, Scrub, FaceCleanser, BodySoap, LiquidSoap, Oil


def home(request):
    body_soaps = BodySoap.objects.all()
    face_cleansers = FaceCleanser.objects.all()
    liquid_soaps = LiquidSoap.objects.all()
    oils = Oil.objects.all()
    scrubs = Scrub.objects.all()
    shampoos = Shampoo.objects.all()

    return render(request, 'home.html', {
        'body_soaps': body_soaps,
        'face_cleansers': face_cleansers,
        'liquid_soaps': liquid_soaps,
        'oils': oils,
        'scrubs': scrubs,
        'shampoos': shampoos,
    })

