#-*- coding: utf-8 -*-

import httplib2
import json
import base64
import csv
import re
from time import sleep

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
    with open('error_data.csv','a') as csvfile:
        fieldnames = []
        fieldnames_dict ={}
        for field in field_name:
            fieldnames.append(field)
        writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
        for data in json_parsed:
            for field in field_name:
                fieldnames_dict[field]=data[field]
            try:
                writer.writerow(fieldnames_dict)
                fieldnames_dict={}
            except UnicodeEncodeError as e:
                try:
                    with open('error_data.csv','a') as csvfile:
                        fieldnames_dict['description'] = fieldnames_dict['description'].encode('utf-8')
                        fieldnames_dict['homepage']=fieldnames_dict['homepage'].encode('utf-8')
                        writer.writerow(fieldnames_dict)
                        fieldnames_dict={}
                    print e
                except AttributeError:
                    print e
error=''

with open('(ywy)error_Top_repositories(final).csv','r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        url='https://api.github.com/search/repositories?q='+row[0]
        print url
        response, content = Request(url)
        json_parsed = json.loads(content)['items']
        WriteCSV(json_parsed,field_list)