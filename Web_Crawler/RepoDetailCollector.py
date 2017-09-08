#-*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib
import csv
import datetime
import time

# Other Language 리스트를 웹에서 불러옴 (콘솔에 출력)
class WebCrawler():
    def __init__(self):
        self.data = {}

    # Request HTML
    def Request(self,owner,repository):
        url = 'https://github.com/'+owner+'/'+repository
        print url
        fp = urllib.urlopen(url)
        source = fp.read()
        fp.close()
        time.sleep(0.2)
        self.request = BeautifulSoup(source, 'html.parser')

    # Scrap Summary
    def SummaryScrap(self):
        while True:
            try:
                summary= self.request.findAll('ul', attrs={'class':'numbers-summary'})
                sumelement = summary[0].find_all('a')
                for ele in sumelement:
                    parsed = ele.text.replace("\n","").strip().replace(" ","")
                    print parsed
                    if ',' in parsed:
                        parsed = parsed.replace(',','')
                    if 'commits' in parsed:
                        value = parsed.replace('commits','')
                        print 'Commits: ' + value
                        self.data['Commit'] = int(value)
                    elif 'branches' in parsed:
                        value = parsed.replace('branches','')
                        print 'Branches: ' + value
                        self.data['Branch'] = int(value)
                    elif 'releases' in parsed:
                        value = parsed.replace('releases','')
                        print 'Releases: ' + value
                        self.data['Release'] = int(value)
                    elif 'contributors' in parsed:
                        value = parsed.replace('contributors','')
                        print 'Contributors: ' + value
                        self.data['Contributor'] = int(value)
                    elif 'license' in parsed:
                        self.data['License']=parsed
                        print 'License: ' + parsed
                    else:
                        print parsed
                break
            except:
                self.Request(owner,repo)
    # Scrap Topics
    def TopicScrap(self):
        self.data['Topic'] = []
        topic = self.request.findAll('div', attrs={'id':'topics-list-container'})
        if topic:
            topicelement = topic[0].find_all('a')
            print 'Topic: '
            for ele in topicelement:
                parsed = ele.text.replace('\n', '').strip()
                self.data['Topic'].append(parsed)
                print parsed
        else:
            print 'no topic'

    # Save Results
    def CSVWrtier(self):
        with open('Repository_data.csv', 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['Commit','Branch','Release','Contributor','License','Topic','Saved_DateTime'])
            writer.writeheader()
            self.data['Saved_DateTime'] = str(datetime.datetime.now())
            writer.writerow(self.data)

repositories = WebCrawler()

# Parse Repository owner and name
with open('data/finalRepoDataCol2.csv','r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        owner,repo = row['full_name'].split('/')
        repositories.Request(owner,repo)
        repositories.SummaryScrap()
        repositories.TopicScrap()
        repositories.CSVWrtier()