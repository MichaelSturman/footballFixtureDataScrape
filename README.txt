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
Something to impliment in the future
