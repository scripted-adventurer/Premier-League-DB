# Premier League DB #

## A Python application to download, store, and display Premier League match data ##

Looking for a simple way to access match data for the current Premier League season? If so, you've just found it. This application contains Python modules to download data from the Premier League API, store it locally in JSON form and in an associated MongoDB instance, and display it using simple command line flags.<br>
<br>
Below is a guide to the application's contents:<br>
<br>
*models.py* contains a reference to the data models used in the application. Currently there is only one collection (matches) though the "ground" field maps to a "ground" sub-object, and the "home_club" and "away_club" fields both map to "club" sub-objects. For the most part these models mirror the fields defined in the Permier League API and are self-explanatory, with a few clarifications:<br>
"kickoff" is the UTC kickoff time of the game, represented as miliseconds in the Unix epoch. <br>
"clock_seconds" is the number of seconds currently on the game's running clock. So if the game is in the 50th minute, this field will be 3000. <br>
"status" is a character with one of three values from the API: 'C' (complete), 'U' (unplayed), 'P' (postponed). <br>
<br>
*settings.py* contains information about the associated MongoDB instance. This file relies on environment variables, so be sure to either set them or replace the contents of the file for use on your own machine.<br>
<br>
*etl.py* contains the logic to extract the data from the Premier League API, transform it by removing unnecessary fields, and load it into the MongoDB instance.<br>
<br>
*pldb.py* contains the primary application logic (invoked at the command line). It currently supports three operations:<br>
--update - downloads and stores API season data (both in the associated database and locally in the "json" folder).<br>
--table - displays the current Premier League standing table (calculated from match information in the database).<br>
--team [team abbr.] - displays information about all matches for a specific team in the season.<br>