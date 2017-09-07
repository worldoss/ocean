#-*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib

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
                self.data['commits'] = int(value)
                print 'Commits: ' + value
            elif 'branches' in parsed:
                value = parsed.replace('branches','')
                self.data['branches'] = int(value)
                print 'Branches: ' + value
            elif 'releases' in parsed:
                value = parsed.replace('releases','')
                self.data['releases'] = int(value)
                print 'Releases: ' + value
            elif 'contributors' in parsed:
                value = parsed.replace('contributors','')
                self.data['contributors'] = int(value)
                print 'Contributors: ' + value
            else:
                self.data['license']=parsed
                print 'License: ' + parsed

    # Scrap Topics
    def TopicScrap(self):
        self.data['topics'] = []
        topic = self.request.findAll('div', attrs={'id':'topics-list-container'})
        topelement = topic[0].find_all('a')
        print 'Topic: '
        for ele in topelement:
            parsed = ele.text.replace('\n','').strip()
            self.data['topics'].append(parsed)
            print parsed

repositories=WebCrawler()
repositories.Request('tensorflow','tensorflow')
repositories.SummaryScrap()
repositories.TopicScrap()
print repositories.data
