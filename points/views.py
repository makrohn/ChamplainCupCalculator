from django.http import HttpResponse
from .models import Points,Event


def index(request):
    points = Points.objects.order_by("competitor_id")
    events = Event.objects.order_by("event_id")
    output = "<br />".join([(q.competitor_id.family_name + ", " + q.competitor_id.given_name) for q in points])
    return HttpResponse(output)
