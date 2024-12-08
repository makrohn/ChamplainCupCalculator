"""A module to take AskFRED results exported from FencingTime, and convert to
Champlain Cup Points System."""

import xml.etree.ElementTree as ET

CUTOFF_MULTIPLIER = 0.8
DEFAULT_MAX_POINTS = 2

tournament_tiers = {
    "tier1": {
        "strengths": ["A4", "A3", "B3"],
        "first_place_points": 32
        },
    "tier2": {
        "strengths": ["A2", "B2", "C3"],
        "first_place_points": 24
        },
    "tier3": {
        "strengths": ["B1"],
        "first_place_points": 20
        },
    "tier4": {
        "strengths": ["C1", "C2"],
        "first_place_points": 16
        },
    "tier5": {
        "strengths": ["D1"],
        "first_place_points": 12
        },
    "tier6": {
        "strengths": ["E1"],
        "first_place_points": 6
        },
    "tier7": {
        "strengths": ["NR"],
        "first_place_points": 3
        },
}

EXCEPTED_RATING_LIMITS = ["Unrated", "EUnder"]
EXCEPTED_AGE_LIMITS = ["VetCombined", "Y12", "Junior"]

class Results(object):
    """The results of a tournament"""
    def __init__(self, ask_fred_file):
        """Open the askFred file and return something Python can use"""
        tree = ET.parse(ask_fred_file)
        root = tree.getroot()
        self.results_data = root
        self.events = {}
        self.tournament_name = self.results_data[0].attrib["Name"]
        self.tournament_date = self.results_data[0].attrib["StartDate"]
        for event in self.results_data[0]:
            rankings = [child.attrib for child in event[0]]
            event_info = event.attrib
            event_info['rankings'] = rankings
            self.events["event" + event_info['EventID']] = event_info
        self.fencers = {}
        for fencer in self.results_data[2]:
            fencer_info = fencer.attrib
            fencer_info['points'] = 0
            self.fencers['fencer' + fencer_info['FencerID']] = fencer_info

    def event_points(self,event_id):
        """Calculate the number of points awarded to each fencer for the event"""
        event = self.events[event_id]
        event_rating = self.events[event_id]['Rating']
        event_gender = self.events[event_id]['Gender']
        event_rating_limit = self.events[event_id]['RatingLimit']
        event_age_limit = self.events[event_id]['AgeLimitMin']
        for tier, stuff in tournament_tiers.items():
            if event_rating in stuff['strengths']:
                event_max_points = stuff['first_place_points']
        if (event_gender != "Mixed" or 
            event_rating_limit in EXCEPTED_RATING_LIMITS or 
            event_age_limit in EXCEPTED_AGE_LIMITS):
            event_max_points = DEFAULT_MAX_POINTS
        bonus_points_cutoff = float(event['Entries']) * CUTOFF_MULTIPLIER
        event_points = []
        for competitor in event['rankings']:
            fencer_id = 'fencer' + competitor['CompetitorID']
            points_awarded = {}
            points_awarded['points'] = 1
            place = int(competitor['Place'])
            cfn = self.fencers[fencer_id]
            points_awarded['first_name'] = cfn['FirstName']
            points_awarded['last_name'] = cfn['LastName']
            points_awarded["fencer_id"] = competitor["CompetitorID"]
            points_awarded["event_id"] = event["EventID"]
            if place < bonus_points_cutoff:
                bonus_points = event_max_points - place + 1
                if bonus_points > 0:
                    points_awarded['points'] += bonus_points
            event_points.append(points_awarded)
        return event_points
