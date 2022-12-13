This code contains a function that takes as arguments a premier league team (required to be in the same format as in the worldfootball.net url), a start date
and an end date and returns details on fixtures.

Limitations/Scope for improvement:
- Need to input the team name in the right format. Could potentially improve using regex pattern matching - one to look at later
- Only pulls in details of games where there is a link to navigate down to lower level details (attendence, players, managers, referee...). Ok 
with this because any future plans I have for this data will require the lower level of detail so would be dropping incomplete data. Most data
is complete with the exception (mainly) of early round FA/League Cup game and Friendly Fixtures
- 'competition' value is locked in to English ones. Could easily be adapted for other leagues with a bit of effort, as the general format
of the data is the same
- No work done to extract team managers. Could be interesting to investigate "new manager bounce" and generally track manager performance.
Something to implement in the future

Output Details
Outputs a CSV file with naming convention (str(start_year) + str(end_year) + teamName) 

Data
Col 1 - uniqueGameId - date.replace("/", "") + homeTeam[0:3] + awayTeam[0:3]. eg 12122020TotArs
Col 2 - competition. eg League Cup
Col 3 - round. eg Semi Final
Col 4 - date eg 12/12/2020
Col 5 - time eg 14:00
Col 6 - home team eg Tottenham Hotspurs
Col 7 - away team eg Arsenal
Col 8 - first half home goals
Col 9 - first half away goals
Col 10 - second half home goals
Col 11 - second half away goals
Col 12 - extra time home goals
Col 13 - extra time away goals
Col 14 - pen shootout home goals
Col 15 - pen shootout away goals
Col 16 - result
Col 17 - venue
Col 18 - city
Col 20 - country
Col 21 - referee
Col 22 - attendance
