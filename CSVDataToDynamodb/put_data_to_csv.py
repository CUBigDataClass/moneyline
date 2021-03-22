import csv
import json
from nba_api.stats.endpoints import boxscoretraditionalv2
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.static import teams
from datetime import timedelta,datetime

r = leaguegamefinder.LeagueGameFinder(date_from_nullable='03/11/2021', league_id_nullable='00').get_normalized_dict()
entries = len(r['LeagueGameFinderResults'])

data_file = open("output.csv", "w", newline='')

counter = 0
for x in r['LeagueGameFinderResults']:
    x = json.loads(json.dumps(x), parse_float=str)
    print(x.values())
    csv_writer = csv.writer(data_file)
    if counter == 0:
        header = x.keys()
        csv_writer.writerow(header)
        counter+=1

    csv_writer.writerow(x.values())

data_file.close()
