# ChamplainCupCalculator
For converting AskFRED results into Champlain Cup Points and Rankings
## Purpose
Every year, the Green Mountain Division hosts the Champlain Cup, to promote participation in Division tournaments. Points are awarded for placing highly in Open events, but also at a reduced rate in limited events.
## Intended awards
* Every participant in every event earns one participation point.
* In events limited by age, gender, or division, or events with rating caps of D or less:
  - 2 additional points to first place, one additional point to second place.
* In all other events:
  - The top 80% of placed fencers earn bonus points.
  - Each place earns one bonus point less than the next higher place.
  - First Place bonus depends on the strength of the event:
    - A4, A3, B3: 32 points
    - A2, B2, C3: 24 points
    - B1: 20 points
    - C1, C2: 16 points
    - D1: 12 points
    - E1: 6 points
## Live-ish Results
Points can currently be found at https://www.gmdfencing.org/points.html
I am lazy and haven't yet set up django to run alongside the WordPress installation there, so right now, I'm loading them all in on my local laptop and then copying the HTML from localhost/points to a static HTML file on the server.
## Loading points
Points are loaded from AskFred files from FencingTime, which are XML formatted. I did it this way because, at the time that I created this, I didn't realize yet that I could download much more straightforward CSV files from AskFred for completed tournaments. Put the .frd file into the same directory as the program, and run a django shell. import cup_load_points, and then use cups_load_points.load_all(file_name, season_name)