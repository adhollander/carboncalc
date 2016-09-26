from django.http import HttpResponse
from django.template import loader

from biomass import biomass_calc
import sqlite3
from api import regionlist, speclist

def jumbotest(request):
    template = loader.get_template('jumbotron.html')
    return HttpResponse(template.render({}, request))

def biomass(request):
    template = loader.get_template('biomass2.html')
    return HttpResponse(template.render({'regions': regionlist, 'species': speclist}, request))



