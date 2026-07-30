from datetime import datetime
import cc_calc
from points.models import Event, Fencer, Points


def load_points_from_csv(file_path: str, season_name: str = "2025-2026") -> None:
    """Loads results using cc_calc.Results and writes to Django DB models."""
    calc_results = cc_calc.Results(file_path)

    for event_key, event_info in calc_results.events.items():
        event_name = event_info["Name"]
        tournament_name = calc_results.tournament_name

        try:
            event_date = datetime.strptime(calc_results.tournament_date, "%Y-%m-%d").date()
        except ValueError:
            event_date = datetime.now().date()

        event_id = f"{tournament_name}_{event_name}"

        # 1. Event DB Object
        event_obj, _ = Event.objects.get_or_create(
            event_id=event_id,
            defaults={
                "event_name": event_name,
                "tournament_name": tournament_name,
                "event_season": season_name,
                "event_date": event_date,
            },
        )

        # 2. Get points awarded list for this event
        calculated_points = calc_results.event_points(event_key)

        for item in calculated_points:
            fencer_id = item["fencer_id"]
            first_name = item["first_name"]
            last_name = item["last_name"]
            pts = item["points"]

            # Fencer DB Object
            fencer_obj, _ = Fencer.objects.get_or_create(
                fencer_id=fencer_id,
                defaults={
                    "given_name": first_name,
                    "family_name": last_name,
                },
            )

            # Points DB Object
            Points.objects.update_or_create(
                competitor_id=fencer_obj,
                event_placed=event_obj,
                defaults={
                    "points": pts,
                },
            )

    print(f"Successfully loaded '{file_path}' into the database!")


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        load_points_from_csv(sys.argv[1])