This code contains a function that takes as arguments a team (required to be in the same format as in the worldfootball.net url), a start date an end date and the country (currently only english teams from prem and championship) and returns details on fixtures.

Limitations/Scope for improvement:
- Need to input the team name in the right format. Could potentially improve using regex pattern matching - one to look at later
- Only pulls in details of games where there is a link to navigate down to lower level details (attendence, players, managers, referee...). Ok 
with this because any future plans I have for this data will require the lower level of detail so would be dropping incomplete data. Most data
is complete with the exception (mainly) of early round FA/League Cup game and Friendly Fixtures
- yet to extend scope to non english leagues/lower english leagues. the latter causes the issue that if we try to get data from a team that dips into those lower leagues at some point during the time span
- No work done to extract team managers. Could be interesting to investigate "new manager bounce" and generally track manager performance.
Something to implement in the future

Output Details
Outputs a CSV file with naming convention (str(start_year) + str(end_year) + teamName) 

Data
Col 1 - uniqueGameId - date.replace("/", "") + homeTeam[0:3] + awayTeam[0:3]. eg 12122020TotArs
Col 2 - season. eg 2001/2002
Col 3 - competition. eg League Cup
Col 4 - round. eg Semi Final
Col 5 - date eg 12/12/2020
Col 6 - time eg 14:00
Col 7 - homeTeam eg Tottenham Hotspurs
Col 8 - awayTeam eg Arsenal
Col 9 - firstHalfGoalsH (first half home goals)
Col 10 - firstHalfGoalsA (first half away goals)
Col 11 - secondHalfGoalsH (second half home goals)
Col 12 - secondHalfGoalsH (second half away goals)
Col 13 - extraTimeGoalsH (extra time home goals)
Col 14 - extraTimeGoalsA (extra time away goals)
Col 15 - penShootoutH (pen shootout home goals)
Col 16 - penShootoutA (pen shootout away goals)
Col 17 - resFT (result) - H (home) A (away) D (draw)
Col 18 - venue
Col 19 - city
Col 20 - country
Col 21 - referee
Col 22 - attendance
