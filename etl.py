import models
import urllib.request
import json
import copy 

class ETL:
  '''Extracts Premier League season data using an HTTP API request,
  transforms it based on the 'match' model defined in models.py, saves the 
  transformed JSON file into json/{season_year}.json and loads it into
  the MongoDB instance pointed to in the settings.py file.''' 
  def __init__(self):
    # HTTP request params
    # think this refers to the league tier (premier league) but other values return
    # no results 
    self.comps = 1
    # returns data from this season (must be set manually)
    self.season_id = 274
    # only return one large page of every match in the season (380 total)
    self.page_num = 0
    self.page_size = 380
    # sort newest to oldest
    self.sort = 'desc'
    # show unplayed, postponed, and complete games
    self.statuses = 'U,P,C'
    # not entirely sure what this does, works as either true or false
    self.alt_ids = 'false'
    self.url = (f"https://footballapi.pulselive.com/football/fixtures?" + 
      f"comps={self.comps}&compSeasons={self.season_id}&" + 
      f"page={self.page_num}&pageSize={self.page_size}&sort={self.page_size}&"
      f"statuses={self.statuses}&altIds={self.alt_ids}")
    self.headers = {'Origin': 'https://www.premierleague.com'}
    # the format to transform to
    self.match = models.match
  def extract(self):
    # request = urllib.request.Request(self.url, self.headers)
    # response = urllib.request.urlopen(request)
    # self.api_data = json.loads(response.read().decode(response.info().get_param(
    #   'charset') or 'utf-8'))
    with open('full_2019_2020.json') as json_file:
      self.api_data = json.load(json_file)
  def transform(self):
    # pull the desired fields from the full season JSON response
    self.transformed = {'matches': []}
    for match in self.api_data[0]['content']:
      this_match = copy.deepcopy(self.match)
      this_match['id'] = match['id']
      this_match['season'] = match['gameweek']['compSeason']['label']
      this_match['gameweek'] = match['gameweek']['gameweek']
      this_match['kickoff'] = match['provisionalKickoff']['millis']
      # doesn't exist for unplayed games
      this_match['clock_seconds'] = (match['clock']['secs'] if 'clock' 
        in match else 0)
      this_match['status'] = match['status']
      this_match['ground']['id'] = match['ground']['id']
      this_match['ground']['name'] = match['ground']['name']
      this_match['ground']['city'] = match['ground']['city']
      this_match['home_club']['id'] = match['teams'][0]['team']['club']['id']
      this_match['home_club']['name'] = match['teams'][0]['team']['club']['name']
      this_match['home_club']['shortName'] = (match['teams'][0]['team']['club']
        ['shortName'])
      this_match['home_club']['abbr'] = match['teams'][0]['team']['club']['abbr']
      # doesn't exist for unplayed games
      this_match['home_goals'] = (match['teams'][0]['score'] if 'score' in 
        match['teams'][0] else 0)
      this_match['away_club']['id'] = match['teams'][1]['team']['club']['id']
      this_match['away_club']['name'] = match['teams'][1]['team']['club']['name']
      this_match['away_club']['shortName'] = (match['teams'][1]['team']['club']
        ['shortName'])
      this_match['away_club']['abbr'] = match['teams'][1]['team']['club']['abbr']
      # doesn't exist for unplayed games
      this_match['away_goals'] = (match['teams'][1]['score'] if 'score' in 
        match['teams'][1] else 0)
      self.transformed['matches'].append(this_match)
  def save_json(self):
    # an optional step to save the transformed JSON file locally
    # set the filename for the transformed json file
    # change the / to - so it's not interpreted as a directory
    self.season_label = (self.api_data[0]['content'][0]['gameweek']['compSeason']
      ['label']).replace('/', '-')
    self.output_file = 'json/' + self.season_label + '.json'
    with open(self.output_file, 'w') as output_file:
      output_file.write(json.dumps(self.transformed, indent=2))
  def load(self):
    pass 
  def run(self):
    self.extract()
    self.transform()
    self.save_json()
    # self.load()  