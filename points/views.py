"""Module to display all adult cup rankings for the Champlain Cup in a web page"""

from operator import itemgetter

from django.http import HttpResponse
from django.template import loader
from .models import Points,Event,Fencer

def get_standings(weapon):
    """Get the standings, along with all points earned, for each fencer for a weapon"""
    points = Points.objects.order_by("competitor_id")

    fencers = Fencer.objects.all()

    events = Event.objects.filter(event_name__contains=weapon).order_by("event_date")

    weapon_events = {}
    cell_id = 1
    for event in events:
        event_values = {}
        event_values['id'] = event.event_id
        event_values['cell_id'] = cell_id
        cell_id += 1
        event_values['tournament'] = event.tournament_name
        weapon_events[event.event_name] = event_values

    weapon_lines = []
    for fencer in fencers:
        row = {}
        fencer_name = fencer.family_name + ", " + fencer.given_name
        row[fencer_name] = {}
        total = 0
        row[fencer_name]['points'] = {}
        points_earned = Points.objects.filter(
            competitor_id=fencer,
            event_placed__event_name__contains=weapon
            )
        for entry in points_earned:
            event_name = entry.event_placed.event_name
            points = entry.points
            position = weapon_events[event_name]['cell_id']
            row[fencer_name]['points'][position] = points
            total += points
        for i in range(1,cell_id):
            if i not in row[fencer_name]['points']:
                row[fencer_name]['points'][i] = 0
        sorted_points = dict(sorted(row[fencer_name]['points'].items()))
        row[fencer_name]['points'] = sorted_points
        row["total"] = total
        if row['total'] != 0:
            weapon_lines.append(row)

    weapon_lines = sorted(weapon_lines, key=itemgetter('total'), reverse=True)
    weapon_results = {}
    weapon_results['events'] = weapon_events
    weapon_results['fencers'] = weapon_lines
    weapon_results['total_events'] = cell_id - 1
    return weapon_results

def index(request):
    """Return several tables with standings for each weapon"""
    context = {}

    epee_standings = get_standings("Epee")
    context['epee'] = epee_standings

    foil_standings = get_standings("Foil")
    context['foil'] = foil_standings

    template = loader.get_template('index.html')
    return HttpResponse(template.render(context, request))
