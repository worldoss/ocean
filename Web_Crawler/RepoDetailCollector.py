#-*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib
import csv
import datetime

# Other Language 리스트를 웹에서 불러옴 (콘솔에 출력)
class WebCrawler():
    def __init__(self):
        self.data = {}

    # Request HTML
    def Request(self,user,repository):
        fp = urllib.urlopen('https://github.com/'+user+'/'+repository)
        source = fp.read()
        fp.close()
        self.request = BeautifulSoup(source, 'html.parser')

    # Scrap Summary
    def SummaryScrap(self):
        summary= self.request.findAll('ul', attrs={'class':'numbers-summary'})
        sumelement = summary[0].find_all('a')
        for ele in sumelement:
            parsed = ele.text.replace("\n","").strip().replace(" ","")
            if ',' in parsed:
                parsed = parsed.replace(',','')
            if 'commits' in parsed:
                value = parsed.replace('commits','')
                self.data['Commit'] = int(value)
                print 'Commits: ' + value
            elif 'branches' in parsed:
                value = parsed.replace('branches','')
                self.data['Branch'] = int(value)
                print 'Branches: ' + value
            elif 'releases' in parsed:
                value = parsed.replace('releases','')
                self.data['Release'] = int(value)
                print 'Releases: ' + value
            elif 'contributors' in parsed:
                value = parsed.replace('contributors','')
                self.data['Contributor'] = int(value)
                print 'Contributors: ' + value
            else:
                self.data['License']=parsed
                print 'License: ' + parsed

    # Scrap Topics
    def TopicScrap(self):
        self.data['Topic'] = []
        topic = self.request.findAll('div', attrs={'id':'topics-list-container'})
        topelement = topic[0].find_all('a')
        print 'Topic: '
        for ele in topelement:
            parsed = ele.text.replace('\n','').strip()
            self.data['Topic'].append(parsed)
            print parsed

    # Save Results
    def CSVWrtier(self):
        with open('Repository_data.csv', 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['Commit','Branch','Release','Contributor','License','Topic','Saved_DateTime'])
            writer.writeheader()
            self.data['Saved_DateTime'] = str(datetime.datetime.now())
            writer.writerow(self.data)

    def RepoParser(self):
        with open('data/finalRepoDataCol2.csv','r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                full_name = row['full_name'].split('/')
                print full_name
                return full_name

repositories=WebCrawler()
user,repo=repositories.RepoParser()
print user, repo
repositories.Request('facebook','react')
repositories.SummaryScrap()
repositories.TopicScrap()
print repositories.data
repositories.CSVWrtier()