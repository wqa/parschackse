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
    #print("Tournament page.")
    r = requests.get(url)
    soup = bs4.BeautifulSoup(r.text, 'html.parser')
    print(soup.prettify())

def analyze_url(url):
    u = urlparse(url)
    if u.path == '/ShowTournamentServlet':
        #print(f"Tournament.")
        analyze_tournament_page(url)
    elif u.path == '/ShowTournamentParticipantResultServlet':
        pass
        #print(f"Participant results in tournament.")
    #print(u)



#url = 'https://member.schack.se/ShowTournamentServlet?id=12754'

#iurl = 'https://member.schack.se/ShowTournamentParticipantResultServlet?id=12754&partid=455826'\
       
#burl = 'https://member.schack.se/ViewPlayerRatingDiagram?memberid=455826'
#analyze_url(url)

# A function that takes a url, retrieves the page and returns a soup object
def get_soup(url):
    result = None
    r = requests.get(url)
    if r.status_code == 200:
        try:
            result = {"error": False, "data": bs4.BeautifulSoup(r.text, 'html.parser')}
        except Exception as e:
            result = {"error": True, "data": f"Error parsing data; status_code=200, Exception: {e}"}
    else:
        result = {"error": True, "data": "Error retrieving data; status_code={r.status_code}"}
    return result

# A function that takes a soup object, loops through all of the tables and all the rows in the tables
# and returns a list of lists with the data simplified as json
# input: soup object
# output: list of lists with data
def get_data(soup):
    # print(soup)
    result = []
    tables = soup.find_all('table')
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            # For each column, both the text and the 'onclick' attibute of the td are extracted
            # then the text and the link are combined into a tuple

            textcols = [col.text.strip() for col in cols]
            onclick_of_all_tds = [col.get('onclick') for col in cols]

            # now combine these two lists into a list of tuples
            cols = list(zip(textcols, onclick_of_all_tds))
            result.append(cols)



    return result

# test the functions
url = 'https://member.schack.se/ShowTournamentServlet?id=12754&partid=455826'
url = 'https://member.schack.se/ShowTournamentRoundResultServlet?id=409027'
url = 'https://member.schack.se/ShowTournamentParticipantResultServlet?id=12772&partid=455826'
soup = get_soup(url)
if soup['error']:
    print(soup['data'])
else:
    data = get_data(soup['data'])

# now loop through the data and print each ROW which includes at least on column
# in which the text contains 'Björn'
for n,row in enumerate(data):
    for col in row:
        row_contains_bjorn = False
        if 'Björn' in col[0]:
            row_contains_bjorn = True
            break
    if row_contains_bjorn:
        if len(row) > 50:
            continue
        rond = row[0][0]
        if rond == '3':
            bord = row[2][0]
            #if bord == 2:
            print(f"{rond} {row[2][0]} {n}; {len(row)}: {row}")
            for c,col in enumerate(row):
                print(f"{c}: {col}")
            break

