import settings
from pymongo import MongoClient
import copy

class Query:
  '''Queries and returns information from the database based on parameters 
  supplied by the user.'''
  def __init__(self):
    self.client = MongoClient(host=settings.database['host'], 
      port=settings.database['port'], username=settings.database['user'], 
      password=settings.database['password'], 
      authSource=settings.database['db'])
    self.db = self.client[settings.database['db']]
  def table(self):
    # calculate and return the current standings table
    club_row = {'club': '', 'matches_played': 0, 'wins': 0,
    'draws': 0, 'losses': 0, 'goal_diff': 0, 'points': 0}
    club_data = {}
    # parse the season data one match at a time, updating stats for each team
    for match in self.db.matches.find({"season": "2019/20", "status": "C"}):
      home = match['home_club']['abbr']
      away = match['away_club']['abbr']
      if away not in club_data:
        club_data[away] = copy.deepcopy(club_row)
        club_data[away]['club'] = away
      if home not in club_data:
        club_data[home] = copy.deepcopy(club_row)
        club_data[home]['club'] = home
      club_data[away]['matches_played'] += 1
      club_data[away]['goal_diff'] += (match['away_goals'] - match['home_goals']) 
      club_data[home]['matches_played'] += 1
      club_data[home]['goal_diff'] += (match['home_goals'] - match['away_goals'])
      if (match['home_goals'] > match['away_goals']):
        club_data[home]['wins'] += 1
        club_data[home]['points'] += 3
        club_data[away]['losses'] += 1
      elif (match['home_goals'] < match['away_goals']):
        club_data[home]['losses'] += 1
        club_data[away]['wins'] += 1
        club_data[away]['points'] += 3
      else:
        club_data[home]['draws'] += 1
        club_data[home]['points'] += 1
        club_data[away]['draws'] += 1
        club_data[away]['points'] += 1
    table = [data for data in club_data.values()]
    table.sort(key= lambda row: row['points'], reverse=True)
    return table 
      
  def club(self, club_abbr):
    # find and return all match data for the specified club  
    matches = self.db.matches.find({"season": "2019/20", "$or": 
      [{"home_club.abbr": club_abbr}, {"away_club.abbr": club_abbr}]}).sort("kickoff")
    return matches