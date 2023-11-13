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
            name = (results.events[event]["AgeLimitMin"] + " " +
                    results.events[event]["Gender"] + " " +
                    results.events[event]["Weapon"]
                    ),
            event = Event(
                event_name = name,
                tournament_name = results.tournament_name,
                event_id = eid,
                event_season = season,
                event_date = results.tournament_date,
            )
            event.save()

def check_fencers(results):
    """Make sure all the fencer exist in the database"""
    for fencer in results.fencers:
        fid = results.fencers[fencer]['FencerID']
        exists = Fencer.objects.filter(fencer_id=fid).exists()
        if exists is False:
            fencer = Fencer(
                fencer_id = fid,
                given_name = results.fencers[fencer]['FirstName'],
                family_name = results.fencers[fencer]['LastName']
            )
            fencer.save()


def check_points(results):
    """Load all the points into the database"""
    for event_results in results.events:
        points_awarded = results.event_points(event_results)
        for entry in points_awarded:
            eid = entry['event_id']
            fid = entry['fencer_id']
            foreign_eid = Event.objects.get(event_id=eid)
            foreign_fid = Fencer.objects.get(fencer_id=fid)
            exists = Points.objects.filter(competitor_id=fid, event_placed=eid).exists()
            points_accrued = Points(
                points=entry['points'],
                competitor_id=foreign_fid,
                event_placed=foreign_eid
            )
            if exists is False:
                points_accrued.save()
            elif exists is True:
                existing_record = Points.objects.get(competitor_id=fid, event_placed=eid)
                existing_record.points=entry['points'],
                existing_record.competitor_id=foreign_fid,
                existing_record.event_placed=foreign_eid
                existing_record.save()
