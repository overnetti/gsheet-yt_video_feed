import re
import time
import urllib.request
from bs4 import BeautifulSoup
from bs4.element import Comment
from urllib.request import urlopen
from collections import defaultdict
import gspread #docs.gspread.org for documentation
from oauth2client.service_account import ServiceAccountCredentials

#Creates list of paper titles.
def bs_title_extraction(html):
    soup = BeautifulSoup(urlopen(html), 'html.parser')
    paper_titles = soup.find_all(href=re.compile('/presentation/'))
    papers_lst = [paper.text for paper in paper_titles]
    while '' in papers_lst:
        papers_lst.remove('')
    return papers_lst 

#Creates list of abstracts for each paper.
def bs_abs_extraction(html):
    soup = BeautifulSoup(urlopen(html), 'html.parser')
    abs_descs = soup.find_all('div', class_='field field-name-field-paper-description-long field-type-text-long field-label-hidden')
    abs_lst = [abs.text for abs in abs_descs]
    return abs_lst 

#Creates a list of authors for each paper.
def bs_author_extraction(html):
    soup = BeautifulSoup(urlopen(html), 'html.parser')
    authors = soup.find_all('div', class_='field field-name-field-paper-people-text field-type-text-long field-label-hidden')
    authors_lst = [auth.text for auth in authors]
    return authors_lst 

#Creates a list of nodes for each paper.
def bs_node_extraction(html):
    soup = BeautifulSoup(urlopen(html), 'html.parser')
    papers_w_node = soup.find_all('article', class_='node node-paper view-mode-schedule')
    nodes_lst = [papers_w_node[x]['id'] for x in range(0, len(papers_w_node))]
    return nodes_lst 

#Feeds each function the link to retrieve data from.
titles = bs_title_extraction('https://www.usenix.org/conference/nsdi23/technical-sessions')
abstracts = bs_abs_extraction('https://www.usenix.org/conference/nsdi23/technical-sessions')
nodes = bs_node_extraction('https://www.usenix.org/conference/nsdi23/technical-sessions')
authors = bs_author_extraction('https://www.usenix.org/conference/nsdi23/technical-sessions')

#Creates Youtube descriptions by looping through the data in each list.
yt_descs = ["NSDI '23 - "+titles[x]+'/n/n'+authors[x]+'/n/n'+abstracts[x]+"/n/nView the full NSDI '23 Technical Sessions at https://www.usenix.org/conference/nsdi23/technical-sessions" for x in range(0, len(abstracts))]

#Maps the data to a dictionary.
category_dict = {}
category_dict['nodes'] = nodes
category_dict['titles'] = titles
category_dict['authors'] = authors
category_dict['abstracts'] = abstracts
category_dict['yt_descs'] = yt_descs

scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('service_credentials.json', scope) #service_credentials can be downloaded using documentation for your workspace
client = gspread.authorize(creds)

#Add the spreadsheet to write to here.
spreadsheet = client.open('YOUR_SPREADSHEETS_NAME')
worksheet = spreadsheet.add_worksheet('yt_feed_import', len(category_dict['nodes']), 4)

#Writes to the Google Sheet.
for row in range(1, len(category_dict['nodes'])+1):
    time.sleep(3) 
    worksheet.update_cell(row, 1, category_dict['nodes'][row-1])
    worksheet.update_cell(row, 2, category_dict['titles'][row-1])
    worksheet.update_cell(row, 3, category_dict['authors'][row-1])
    worksheet.update_cell(row, 4, category_dict['yt_descs'][row-1])
