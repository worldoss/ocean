#-*- coding: utf-8 -*-

import httplib2
import json
import base64
import csv
import re
from time import sleep

class incompleteError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

class NoresultError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

language=[
    'ActionScript',
    'C',
    'CSharp',
    'CPP',
    'Clojure',
    'CoffeeScript',
    'CSS',
    'Go',
    'Haskell',
    'HTML',
    'Java',
    'Javascript',
    'Lua',
    'Matlab',
    'Objective-C',
    'Perl',
    'PHP',
    'Python',
    'R',
    'Ruby',
    'Scala',
    'Shell',
    'Swift',
    'TeX',
    'Vim-script'
]

field_list=[
    'id','name','full_name',
    'owner','private','html_url',
    'description','fork','url',
    'forks_url','keys_url','keys_url',
    'collaborators_url','teams_url','hooks_url',
    'issue_events_url','events_url','assignees_url',
    'branches_url','tags_url','blobs_url',
    'git_tags_url','git_refs_url','trees_url',
    'statuses_url','languages_url','stargazers_url',
    'contributors_url','subscribers_url','subscription_url',
    'commits_url','git_commits_url','comments_url',
    'issue_comment_url','contents_url','compare_url',
    'merges_url','archive_url','downloads_url',
    'issues_url','pulls_url','milestones_url',
    'notifications_url','labels_url','releases_url',
    'deployments_url','created_at','updated_at',
    'pushed_at','git_url','ssh_url',
    'clone_url','svn_url','homepage',
    'size','stargazers_count','watchers_count',
    'language','has_issues','has_projects',
    'has_downloads','has_wiki','has_pages',
    'forks_count','mirror_url','open_issues_count',
    'forks','open_issues','watchers',
    'default_branch','permissions','score'
]

def Request(url):
    http = httplib2.Http()
    auth = base64.encodestring('rlrlaa123' + ':' + 'ehehdd009')
    return http.request(url,'GET',headers={ 'Authorization' : 'Basic ' + auth})

def WriteCSV(json_parsed,field_name):
    with open('data/1000_star_per_repository_language.csv','a') as csvfile:
        fieldnames = []
        fieldnames_dict = {}
        for field in field_name:
            fieldnames.append(field)
        writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
        for data in json_parsed:
            for field in field_name:
                fieldnames_dict[field]=data[field]
            try:
                writer.writerow(fieldnames_dict)
                fieldnames_dict = {}
            except UnicodeEncodeError as e1:
                with open('data/(test)error_language_1000.csv','a') as csvfile:
                    fieldnames_dict['description']=fieldnames_dict['description'].encode('utf-8')
                    try:
                        writer.writerow(fieldnames_dict)
                        fieldnames_dict = {}
                    except UnicodeEncodeError as e2:
                        errorwriter = csv.writer(csvfile)
                        errorwriter.writerow([fieldnames_dict['full_name'],e2])
                        writer.writerow({})
                        fieldnames_dict = {}


def FindLink(response,which):
    if which == 'next':
        return re.compile('([0-9]+)>; rel="next"').findall(response['link'])
    elif which == 'last':
        return re.compile('([0-9]+)>; rel="last"').findall(response['link'])

def NextPage(url,next,last):
    count_last = 2
    while count_last<int(last[0])+1:
        try:
            next_url = url + '&page=' + str(next[0])
            print next_url
            response, content = Request(next_url)
            if json.loads(content)['incomplete_results'] == False:
                json_parsed = json.loads(content)['items']
                WriteCSV(json_parsed,['language','stargazers_count'])
                next = FindLink(response,'next')
                count_last += 1
            else:
                raise incompleteError('Not incomplete results, try again')
        except incompleteError as e:
            print e
        except KeyError as e:
            print e
            sleep(2)

# Star Count First top 1000 stars respositories per language
for lang in language:
    while True:
        url = 'https://api.github.com/search/repositories?q=stars:>5+language:"'+lang+'"&per_page=100&sort=stars'
        print url
        try:
            response, content = Request(url)
            if json.loads(content)['incomplete_results']==False:
                json_parsed = json.loads(content)['items']
                WriteCSV(json_parsed,['language','stargazers_count'])
                try:
                    next = FindLink(response,'next')
                    NextPage(url,next,[10])
                    break
                except KeyError as e:
                    print e
            else:
                raise incompleteError('Not incomplete results, try again')
        except KeyError as e:
            print e
            sleep(2)


