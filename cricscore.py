import urllib
import xml.etree.ElementTree as ET
import sys
import json

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

print(team_id[score['score']['batting']['id']] + " " + score['score']['batting']['score'])
print(score['status'])

