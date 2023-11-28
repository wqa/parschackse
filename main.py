#!/usr/bin/python3
from urllib.parse import urlparse

import requests
import bs4
import sys


#args = sys.argv
#if len(args) != 2:
#    print('Usage: python3 main.py <url>')
#    sys.exit(1)

#url = args[1]


def analyze_tournament_page(url):
    print("Tournament page.")
    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    print(soup.prettify())

def analyze_url(url):
    u = urlparse(url)
    if u.path == '/ShowTournamentServlet':
        print(f"Tournament.")
        analyze_tournament_page(url)
    elif u.path == '/ShowTournamentParticipantResultServlet':
        print(f"Participant results in tournament.")
    print(u)



url = 'https://member.schack.se/ShowTournamentServlet?id=12754'

iurl = 'https://member.schack.se/ShowTournamentParticipantResultServlet?id=12754&partid=455826'\
       
burl = 'https://member.schack.se/ViewPlayerRatingDiagram?memberid=455826'
analyze_url(url)
