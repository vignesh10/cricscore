import urllib
import xml.etree.ElementTree as ET
import sys
import json
from prettytable import PrettyTable

resp_xml = urllib.urlopen('http://www.cricbuzz.com/api/html/matches-menu').read().replace('&nbsp;','')

nav = ET.fromstring(resp_xml).find('nav')

matches = []
match_ids = []

for child in nav:
    if "cb-mat-mnu-itm cb-ovr-flo" in child.attrib.values():
        matches.append(child.text)
        start_index = child.attrib['href'][1:].find('/')+2
        end_index = start_index + child.attrib['href'][start_index:].find('/')
        match_ids.append(child.attrib['href'][start_index:end_index])

print("SELECT THE MATCH\n")

for i in range(len(matches)):
    print(str(i+1) + '.' + ' ' + matches[i])

choice = raw_input("Enter your choice (Enter 'q' to quit): ")

if choice=='q':
    sys.exit(0)

choice = int(choice)

while choice<1 or choice>len(match_ids):
    choice = int(raw_input("Please enter a number between 1 and %d:"%(len(urls))))

choice -= 1    

#print("http://www.cricbuzz.com/match-api/" + match_ids[choice] + "/commentary.json")
resp_json = urllib.urlopen("http://www.cricbuzz.com/match-api/" + match_ids[choice] + "/commentary.json").read()

score = json.loads(resp_json)
print("Location: " + score['venue']['name'] + ", " + score['venue']['location'])

team_id =  {}
team_id[str(score['team1']['id'])] = score['team1']['name']
team_id[str(score['team2']['id'])] = score['team2']['name']

player = {}
for i in range(len(score['players'])):
    player[str(score['players'][i]['id'])] = score['players'][i]['f_name']

print('\n\n')
print('=========================='+team_id[score['score']['batting']['id']] + " " + score['score']['batting']['score']+'==========================')
score_table = PrettyTable(['Batsman','Runs','Balls','Fours','Sixes','Strike Rate'])

for i in range(2):
    batsman = player[str(score['score']['batsman'][i]['id'])]
    if score['score']['batsman'][i]['strike']=='1':
        batsman += '*'
    runs = score['score']['batsman'][i]['r']
    balls = score['score']['batsman'][i]['b']
    fours = score['score']['batsman'][i]['4s']
    sixes = score['score']['batsman'][i]['6s']
    strike_rate = (float(runs)/float(balls))*100.0
    strike_rate = format(strike_rate,'.2f')
    score_table.add_row([batsman,runs,balls,fours,sixes,strike_rate])

print score_table   

print('\nBowling')
bowling_table = PrettyTable(['Bowler','Overs','Maidens','Runs','Wickets'])

for i in range(2):
    bowler = player[str(score['score']['bowler'][i]['id'])]
    overs = score['score']['bowler'][i]['o']
    maidens = score['score']['bowler'][i]['m']
    runs = score['score']['bowler'][i]['r']
    wickets = score['score']['bowler'][i]['w']
    bowling_table.add_row([bowler,overs,maidens,runs,wickets])

print bowling_table
print(score['status'])

