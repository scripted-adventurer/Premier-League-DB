from etl import ETL
from query import Query
import argparse
import datetime

def main():
  parser = argparse.ArgumentParser(description='CLI for the pldb application.')
  parser.add_argument('--update', action='store_true', 
    help='Download season data and update the JSON file and the database.')
  parser.add_argument('--table', action='store_true', 
    help='Display the current standings table (calculated from data in the database).')
  parser.add_argument('--club', type=str, default=None, 
    help='Display info for all the matches for the given club in the season.')
  args = parser.parse_args()
  
  if args.update:
    print("Updating season data...")
    etl = ETL()
    etl.run()
    print("done.")
  elif args.table:
    query = Query()
    table_data = query.table()
    print("#\tClub\tPlayed\tWon\tDrawn\tLost\tGD\tPoints")
    for rank in range(len(table_data)):
      row = table_data[rank]
      print(f"{rank + 1}\t{row['club']}\t{row['matches_played']}\t" 
        f"{row['wins']}\t{row['draws']}\t{row['losses']}\t{row['goal_diff']}\t"
        f"{row['points']}")
  elif args.club:
    query = Query()
    for match in query.club(args.club):
      kick_time = match['kickoff'] / 1000
      kick_time = datetime.datetime.fromtimestamp(kick_time).strftime("%a %d %b %H:%M")
      if match['status'] == 'C':
        score = f"{match['away_goals']} {match['home_goals']}"
      else:
        score = ' @ '  
      print(f"{kick_time} {match['away_club']['abbr']} "
        f"{score} {match['home_club']['abbr']} {match['ground']['name']}")
  
if __name__ == '__main__':
  main()