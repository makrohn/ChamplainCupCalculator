"""Module to load an AskFRED results file into the Database"""

import cc_calc
from points.models import Fencer,Event,Points

def load_results(ask_fred_file):
    """Parse the results into something we can use"""
    results = cc_calc.Results(ask_fred_file)
    return results

def check_events(results, season):
    """Make sure all the events exist in the database"""
    for event in results.events:
        eid = results.events[event]["EventID"]
        exists = Event.objects.filter(event_id=eid).exists()
        if exists is False:
            weapon = results.events[event]["Weapon"]
            rating_limit = results.events[event]["RatingLimit"]
            gender = results.events[event]["Gender"]
            age_limit = results.events[event]["AgeLimitMin"]
            if gender != "Mixed":
                gender = gender + "'s"
            name = gender + " " + weapon
            if age_limit != "None":
                name =  age_limit + " " + name
            if rating_limit != "None":
                name = rating_limit + " " + name
            event_details = Event(
                event_name = name,
                tournament_name = results.tournament_name,
                event_id = eid,
                event_season = season,
                event_date = results.tournament_date,
            )
            event_details.save()

def check_fencers(results):
    """Make sure all the fencer exist in the database"""
    for fencer in results.fencers:
        fid = results.fencers[fencer]['FencerID']

        Fencer.objects.get_or_create(fencer_id=fid, defaults={
            'given_name': results.fencers[fencer]['FirstName'],
            'family_name': results.fencers[fencer]['LastName']
        })


def check_points(results):
    """Load all the points into the database"""
    for event_results in results.events:
        points_awarded = results.event_points(event_results)
        for entry in points_awarded:
            eid = entry['event_id']
            fid = entry['fencer_id']
            foreign_eid = Event.objects.get(event_id=eid)
            foreign_fid = Fencer.objects.get(fencer_id=fid)
            
            Points.objects.update_or_create(
                competitor_id=foreign_fid,
                event_placed=foreign_eid,
                defaults={'points': entry['points']}
            )

def load_all(file, season):
    """Load everything in a file"""
    results = load_results(file)
    check_events(results, season)
    check_fencers(results)
    check_points(results)
