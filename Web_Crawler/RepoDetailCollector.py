#-*- coding: utf-8 -*-

# version 1.2

# 예상소요시간: 약 70시간

from bs4 import BeautifulSoup
import requests
import csv
import datetime
import time
import re

class NoResultError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

# Other Language 리스트를 웹에서 불러옴 (콘솔에 출력)
class WebCrawler():
    def __init__(self,save_file,error_file,final_file):
        self.data = {}
        self.field_list = [
            'full_name',
            'Commit',
            'Branch',
            'Release',
            'Contributor',
            'Topic',
            'Saved_DateTime'
        ]
        self.save_file = save_file
        self.error_file = error_file
        self.final_file = final_file
    # Request HTML
    def Request(self,owner,repository):
        url = 'https://github.com/'+owner+'/'+repository
        print (url)
        fp = requests.get(url)
        # fp = urllib.urlopen(url)
        source = fp.text

        if source == 'Not Found':
            raise NoResultError('No result Found')

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

                print ('Commits: ' + value)
                self.data['Commit'] = int(value)

            elif 'commit' in parsed:
                value = parsed.replace('commit','')

                print ('Commits: ' + value)
                self.data['Commit'] = int(value)

            elif 'branches' in parsed:
                value = parsed.replace('branches','')

                print ('Branches: ' + value)
                self.data['Branch'] = int(value)

            elif 'branch' in parsed:
                value = parsed.replace('branch','')

                print ('Branches: ' + value)
                self.data['Branch'] = int(value)

            elif 'releases' in parsed:
                value = parsed.replace('releases','')

                print ('Releases: ' + value)
                self.data['Release'] = int(value)

            elif 'release' in parsed:
                value = parsed.replace('release','')

                print ('Releases: ' + value)
                self.data['Release'] = int(value)

            elif 'contributors' in parsed:
                try:
                    value = parsed.replace('contributors', '')

                    print ('Contributors: ' + value)
                    self.data['Contributor'] = int(value)

                except ValueError as e:
                    print ('Fetching Error')

            elif 'contributor' in parsed:
                try:
                    value = parsed.replace('contributor', '')

                    print ('Contributors: ' + value)
                    self.data['Contributor'] = int(value)

                except ValueError as e:
                    print ('Fetching Error')
            # else:
            #     self.data['License'] = parsed
            #     print (parsed)
    # Scrap Topics
    def TopicScrap(self):
        self.data['Topic'] = []
        topic = self.request.findAll('div', attrs={'id':'topics-list-container'})
        if topic:
            topicelement = topic[0].find_all('a')
            print ('Topic: ')
            for ele in topicelement:
                parsed = ele.text.replace('\n', '').strip().encode('ascii')
                parsed = parsed.decode('utf-8')
                self.data['Topic'].append(parsed)
                print (parsed)
        else:
            print ('no topic')
    # Create Save File
    def CSVCreater(self):
        with open(self.save_file, 'a') as csvfile:
            writer = csv.DictWriter(csvfile,fieldnames=self.field_list)
            writer.writeheader()
    # Save Results
    def CSVWrtier(self):
        print (self.data)
        with open(self.save_file, 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.field_list)
            self.data['Saved_DateTime'] = str(datetime.datetime.now())
            writer.writerow(self.data)
    # Write Error Repositories
    def ErrorWriter(self,fullname):
        with open(self.error_file, 'a') as csvfile:
            errorwriter = csv.writer(csvfile)
            errorwriter.writerow([fullname])
        with open(self.error_file,'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.field_list)
            for field in self.field_list:
                self.data[field] = 'null'
            self.data['full_name'] = fullname
            self.data['Topic'] = []
            self.data['Saved_DateTime'] = str(datetime.datetime.now())
            writer.writerow(self.data)

    def Topic_Parser(self):
        with open(self.final_file, 'a') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['full_name', 'Commit', 'Branch', 'Release', 'Contributor', 'Topic'])

        with open(self.save_file, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                regex = re.compile("'(.+?)'")
                topic = regex.findall(row['Topic'])
                with open(self.final_file, 'a') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(
                        [row['full_name'], row['Commit'], row['Branch'], row['Release'], row['Contributor']] + topic)