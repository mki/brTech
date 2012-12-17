from django.shortcuts import render_to_response
from django.template import RequestContext
from django.shortcuts import Http404

from main.models import Country
from main.models import City
from main.models import Airport


def index(request):
    country = Country.objects

    return render_to_response('country.html', {'Country': country},
        context_instance=RequestContext(request))


def cities(request, slug=''):
    try:
        city = City.objects(country=Country.objects(slug=slug)[0])
    except:
        raise Http404

    return render_to_response('city.html', {'City': city, 'slug': slug},
        context_instance=RequestContext(request))


def airports(request, slug=''):
    try:
        city=City.objects(slug=slug)[0]
        airport = Airport.objects(city=city)
    except:
        raise Http404

    return render_to_response('airport.html', {'Airport': airport, 'slug': slug, 'city': city},
        context_instance=RequestContext(request))


def airports_info(request, slug=''):
    try:
        airport = Airport.objects(slug=slug)[0]
    except:
        raise Http404

    return render_to_response('airport_info.html', {'Airport': airport},
        context_instance=RequestContext(request))

