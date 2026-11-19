import random

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render

from .models import PITAirportTrainFact


def hello(request):
    return HttpResponse("Hello World from PIT Airport Train App!")


def facts_json(request):
    data = list(PITAirportTrainFact.objects.values())
    return JsonResponse(data, safe=False)


def random_fact_page(request):
    facts = PITAirportTrainFact.objects.all()
    if not facts.exists():
        return render(request, "random_fact_page.html", {"fact": None})

    fact = random.choice(facts)
    return render(request, "random_fact_page.html", {"fact": fact})


def random_fact_json(request):
    facts = PITAirportTrainFact.objects.all()
    if not facts.exists():
        return JsonResponse({"error": "No fun facts found"}, status=404)

    fact = random.choice(facts)
    return JsonResponse({
        "id": fact.id,
        "fun_fact": fact.funFact,
        "date_added": fact.dateAdded,
    })
