import bs4
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

import warnings
warnings.filterwarnings("ignore")


# First attempt made from ESPN website, but came to life that the attendence figures are very patchy. Will be using 
# the https://www.worldfootball.net/teams/tottenham-hotspur/2022/3/ site this time - data goes back further and has 
# complete attendence figures from the exploratory analysis performed.

# Rows with length 15 --> keys, rows with length 3 seem to be links to other pages (club, competition...)
# All else is 17, these are the ones we want

# Analysis of the 17 rows:
# 0 - Empty
# 1 - Title of the competition (friendlies clubs 21, PL, etc
# 2 - Empty
# 3 - Date of the match
# 4 - Empty
# 5 - Time of the match
# 6 - Empty
# 7 - A/H [for Tottenham/team whos page we are on]
# 8 - Empty
# 9 - Image of the opposition badge
# 10 - Empty
# 11 - Opposition name
# 12 - Empty
# 13 - Score. In brackets --> half time, outside --> final score. More complicated for EAT/pens. Look at later
# 14 - Empty
# 15 - No relevant data 
# 16 - Empty

def teamRange(yearStart, yearEnd, team):

    teamWords = team.split('-')
    teamName = ""
    for word in teamWords:
        if word != "fc":
            word = word.capitalize()
            teamName += word + " "
    
    print(teamName)

    cols = {"uniqueID": [], "competition": [], "round": [], "date": [], "time": [], "homeTeam": [], "awayTeam": [], "firstHalfGoalsH": [],
        "firstHalfGoalsA": [], "secondHalfGoalsH": [], "secondHalfGoalsA": [], "extraTimeGoalsH": [], "extraTimeGoalsA": [], 
        "penShootoutH": [], "penShootoutA": [], "resFT": [],  "venue": [], "city": [], "country": [], "referee": [], 
        "attendance": []}

    fixtureData = pd.DataFrame(cols)

    stemURL = "https://www.worldfootball.net"

    for yr in range(yearStart, yearEnd):
        
        print(yr)
        url = stemURL + "/teams/"+ team + "/" + str(yr) + "/3/"
        soup = BeautifulSoup(requests.get(url).text, "html.parser")
        tableRows = soup.find_all('tr')

        for i in range(0, len(tableRows)):    
            if len(tableRows[i]) > 15:
                if tableRows[i].contents[1].contents[0]['title'][0:6] != "Friend":
                    competition = tableRows[i].contents[1].contents[0]['title']

                    # Reformat competiton using regex pattern match. Considers only English teams that have been
                    # only in the prem. 
                    round = 'N/A'

                    if (re.search('.*Premier League.*', str(competition)) != None):
                        competition = 'Premier League'
                    
                    elif (re.search('.*Champions League.*', str(competition)) != None):
                        round = competition.replace('Champions League', "").replace(str(yr), "").replace(str(yr-1), "").replace("/", "")
                        competition = 'Champions League'
                    
                    elif (re.search('.*League Cup.*', str(competition)) != None):
                        round = competition.replace('League Cup', "").replace(str(yr), "").replace(str(yr-1), "").replace("/", "")
                        competition = 'League Cup'
                    
                    elif (re.search('.*FA Cup.*', str(competition)) != None):
                        round = competition.replace('FA Cup', "").replace(str(yr), "").replace(str(yr-1), "").replace("/", "")
                        competition = 'FA Cup'

                    elif (re.search('.*Europa League.*', str(competition)) != None):
                        round = competition.replace('Europa League', "").replace(str(yr), "").replace(str(yr-1), "").replace("/", "")
                        competition = 'Europa League'
                    
                    elif (re.search('.*Conference League.*', str(competition)) != None):
                        round = competition.replace('Europa Conference League', "").replace(str(yr), "").replace(str(yr-1), "").replace("/", "")
                        competition = 'Europa Conference League' 

                    elif (re.search(".*Cup Winners Cup.*", str(competition)) != None):
                        round = competition.replace('Cup Winners Cup', "").replace(str(yr), "").replace(str(yr-1), "").replace("/", "")
                        competition = 'Cup Winners Cup'
                    
                    else:
                        pass

                    date = tableRows[i].contents[3].contents[0].contents[0]

                    if len(tableRows[i].contents[5].contents) == 1:
                        time = tableRows[i].contents[5].contents[0]
                    elif len(tableRows[i].contents[5].contents) == 0:
                        time = "Null"
                    else:
                        "something wrong - Time"
                        break

                    if tableRows[i].contents[7].contents[0] == "A":
                        homeTeam = tableRows[i].contents[11].contents[1].contents[0]
                        awayTeam = teamName
                    elif tableRows[i].contents[7].contents[0] == "H":
                        homeTeam = teamName
                        awayTeam = tableRows[i].contents[11].contents[1].contents[0]           
                    # N - playing a stadium which is neither team's home. Just put the team looped over as home
                    elif(tableRows[i].contents[7].contents[0] == "N"):
                        homeTeam = teamName
                        awayTeam = tableRows[i].contents[11].contents[1].contents[0]           
                    else:
                        print("something wrong - Home/Away Teams")
                        break

                    # figuring out scores (fiddly with pso/aet etc)
                    # also - the scores have the team whos page you are ons goals first regardless of H/A.
                    # flip the strings where appropriate
                    try:
                        scores = tableRows[i].contents[13].contents[1].contents[0].split(" ")
                    except:
                        break

                    scoresArr = []

                    for score in scores:
                        score = score.replace(")", "").replace("(", "").replace(",", "")
                        if len(score) > 1:
                            if tableRows[i].contents[7].contents[0] == "A":
                                scoresArr.append(score[::-1])
                            else:
                                scoresArr.append(score)

                    # Bog standard first half second half 
                    extraTimeHomeGoals = extraTimeAwayGoals = penHomeGoals = penAwayGoals = 'Null'
                    
                    if len(scoresArr) == 2:
                        halfTimeScore = scoresArr[1].split(':')
                        fullTimeScore = scoresArr[0].split(':')
                        
                        halfTimeHomeGoals = halfTimeScore[0]
                        halfTimeAwayGoals = halfTimeScore[1]
                        fullTimeHomeGoals = fullTimeScore[0]
                        fullTimeAwayGoals = fullTimeScore[1]

                        result = "H" if fullTimeHomeGoals > fullTimeAwayGoals else "A" if fullTimeAwayGoals > fullTimeHomeGoals else "D"

                                
                    elif len(scoresArr) == 4:
                        # Games where we go straight from ordinary time to pens (tottenham wolves league cup third round))
                        halfTimeScore = scoresArr[1].split(':')
                        fullTimeScore = scoresArr[2].split(':')

                        halfTimeHomeGoals = halfTimeScore[0]
                        halfTimeAwayGoals = halfTimeScore[1]
                        fullTimeHomeGoals = fullTimeScore[0]
                        fullTimeAwayGoals = fullTimeScore[1]

                        # Accounting for if we needed to reverse the scores
                        if scoresArr[3] == 'osp' or scoresArr[3] == 'pso':                 
                            penaltyScore = scoresArr[0].split(':')
                            penHomeGoals = penaltyScore[0]
                            penAwayGoals = penaltyScore[1]
                            # Result of a game decided on a shoot out can either be a win or a loss
                            result = "H" if penHomeGoals > penAwayGoals else "A"

                        # Games where a team scores a winner in added extra time (middlesborough tottenham FA cup...)
                        if scoresArr[3] == 'tea' or scoresArr[3] == 'aet':
                            extraTimeScore = scoresArr[0].split(':')
                            extraTimeHomeGoals = extraTimeScore[0]
                            extraTimeAwayGoals = extraTimeScore[1]
                            # Result of a game decided in extra time can either be a win or a loss
                            result = "H" if extraTimeHomeGoals > extraTimeAwayGoals else "A"

                    
                    # Hypothetical as can't find for spurs - if we go through first half second half aet and pens
                    elif len(scoresArr) == 5:
                        halfTimeScore = scoresArr[1].split(':')
                        fullTimeScore = scoresArr[2].split(':')
                        extraTimeScore = scoresArr[3].split(':')
                        penaltyScore = scoresArr[0].split(':')

                        halfTimeHomeGoals = halfTimeScore[0]
                        halfTimeAwayGoals = halfTimeScore[1]
                        fullTimeHomeGoals = fullTimeScore[0]
                        fullTimeAwayGoals = fullTimeScore[1]
                        extraTimeHomeGoals = extraTimeScore[0]
                        extraTimeAwayGoals = extraTimeScore[1]
                        penHomeGoals = penaltyScore[0]
                        penAwayGoals = penaltyScore[1]

                        result = "H" if penHomeGoals > penAwayGoals else "A"
                    else:
                        halfTimeHomeGoals = halfTimeAwayGoals = fullTimeHomeGoals = fullTimeAwayGoals = 'Null'
                    
                    gameLink = stemURL + tableRows[i].contents[13].contents[1]['href']

                    # More granular details - mainly concerned with the attendance and the location
                    matchPage = BeautifulSoup(requests.get(gameLink).text, "html.parser")

                    # Define attendance outside the loop so we have an empty string for missing data
                    attendance = ''
                    for row in matchPage.find_all('tr'):              
                        if len(row) ==7:

                            # Location data and venue
                            if re.search('.*venues.*', str(row.contents[5].contents[0])) != None:
                                venue = row.contents[5].contents[0]['title'].split("(")

                                # Ran into an error where the stadium name had a brace in it - this 
                                # solution drops whatever was in brackets, but keeps the rest
                                location = venue[len(venue) - 1].replace(")", "").split("/")
                                for i in range(0, len(location)):
                                    location[i] = location[i].replace(" ", "").replace(")", "")        
                                country = location[1]
                                venue = venue[0]
                                city = location[0]

                            # Don't particularly care about assistant referees at the moment, but could easily append
                            if (re.search('.*Referee.*', str(row.contents[5].contents[0])) != None and 
                                re.search('.*Assistant.*', str(row.contents[5].contents[0]['title'])) == None):
                                referee = row.contents[5].contents[0]['title'].replace("Referee ", "")

                            # Attendance 
                            if(re.search('[0-9].*\..*[0-9]', str(row.contents[5].contents[0])) != None):
                                attendance += (row.contents[5].contents[0].replace("\n", "").replace(".", ""))

                        else:
                            pass
                    
                    print(len(matchPage.find_all('tr')))

                    # First test - Tottenham VS Rennes we have a first row found with length 11 - lots of info we don't need
                    # Second row has length 6 - also don't need, formatting and more titles
                    # The rest have lengths 3, 5 and 7 (3, 6, 52). 63 total 'tr' tags.

                    # Second test - Tottenham VS Mura - again first row length 11 containing titles. Second row also length 6.
                    # Remainder lengths 3, 5 and 7 (3 8 and 53). 66 total 'tr' tags.

                    # Third Test - Tottenham vs Aston Villa. Same rows of 11 and 6 in spaces 0 and 1 respectively. 
                    # Remainder lengths 3, 5 and 7 (3, 6 and 47). 58 total 'tr' tags.

                    # Looks like we can ignore the first 2 tags. Next step is figuring out what the 5s and 7s are respectively.
                    # Intuitively I think the 5s will be the game data (location, attendence) and the 7s the player data.

                    # From inspection, 5 seems to be our player data, manager data and data on who scored. Length 3 formatting
                    # information for the table. 

                    print({'uniqueID': date.replace("/", "") + homeTeam[0:3] + awayTeam[0:3], 'competition': competition, 'round': round,
                                        'date': date, 'time': time, 'homeTeam': homeTeam, 'awayTeam': awayTeam, 'firstHalfGoalsH': halfTimeHomeGoals,
                                        'firstHalfGoalsA': halfTimeAwayGoals, 'secondHalfGoalsH': fullTimeHomeGoals , 'secondHalfGoalsA': fullTimeAwayGoals,
                                        'extraTimeGoalsH': extraTimeHomeGoals,  'extraTimeGoalsA': extraTimeAwayGoals, 'penShootoutH': penHomeGoals, 
                                        'penShootoutA': penAwayGoals, 'resFT': result, 'venue': venue, 'city': city, 'country': country, 'referee': referee, 
                                        'attendance': attendance})

                    fixtureData = pd.concat([fixtureData, pd.DataFrame.from_records([{'uniqueID': date.replace("/", "") + homeTeam[0:3] + awayTeam[0:3], 'competition': competition, 'round': round,
                                        'date': date, 'time': time, 'homeTeam': homeTeam, 'awayTeam': awayTeam, 'firstHalfGoalsH': halfTimeHomeGoals,
                                        'firstHalfGoalsA': halfTimeAwayGoals, 'secondHalfGoalsH': fullTimeHomeGoals , 'secondHalfGoalsA': fullTimeAwayGoals,
                                        'extraTimeGoalsH': extraTimeHomeGoals,  'extraTimeGoalsA': extraTimeAwayGoals, 'penShootoutH': penHomeGoals, 
                                        'penShootoutA': penAwayGoals, 'resFT': result, 'venue': venue, 'city': city, 'country': country, 'referee': referee, 
                                        'attendance': attendance}])])

                else:
                    pass
    return fixtureData

def main(): 

    startDate = 2000
    endDate = 2022
    teams = ["chelsea-fc", "manchester-united", "liverpool-fc", "manchester-city"]

    for team in teams:
        output = teamRange(startDate, endDate, team)
        output.to_csv(str(startDate) + str(endDate) + team + ".csv", encoding='utf-8')

if __name__ == "__main__":
    main()

