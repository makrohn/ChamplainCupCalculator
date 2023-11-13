import cc_calc
from points.models import Fencer,Event,Points

def load_results(askFredFile):
    results = cc_calc.Results(askFredFile)
    return results

def check_events(results, season):
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
    
# for event_results in results.events:
#     points_awarded = results.event_points(event_results)