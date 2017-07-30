#-*- coding: utf-8 -*-

import httplib2
import json
import base64
import csv
import re
from time import sleep

def request(url):
    http = httplib2.Http()
    auth = base64.encodestring('rlrlaa123' + ':' + 'ehehdd009')
    return http.request(url,'GET',headers={ 'Authorization' : 'Basic ' + auth})

def write_csv(filename,json_data,*args):
    with open(filename,'a') as csvfile:
        fieldnames = []
        fieldnames_dict = {}
        for field in args:
            fieldnames.append(field)
        writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
        for data in json_data:
            for field in args:
                fieldnames_dict[field]=data[field]
            try:
                writer.writerow(fieldnames_dict)
                fieldnames_dict = {}
            except UnicodeEncodeError as e1:
                with open('data/(test)error_repository.csv','a') as csvfile:
                    errorwriter = csv.writer(csvfile)
                    errorwriter.writerow([fieldnames_dict['full_name'],e1])
                    fieldnames_dict['description']=fieldnames_dict['description'].encode('utf-8')
                    try:
                        writer.writerow(fieldnames_dict)
                        fieldnames_dict = {}
                    except UnicodeEncodeError as e2:
                        errorwriter.writerow([])
                        errorwriter.writerow([fieldnames_dict['full_name'],'',e2])
                        errorwriter.writerow([])
                        writer.writerow({})
                        fieldnames_dict = {}


def find_link(response,which):
    if which == 'next':
        return re.compile('([0-9]+)>; rel="next"').findall(response['link'])
    else:
        return re.compile('([0-9]+)>; rel="last"').findall(response['link'])

def next_page(next,last,url):
    count_last = 2
    while count_last<int(last[0]):
        try:
            next_url = url + '&page=' + str(next[0])
            response, content = request(next_url)
            if json.loads(content)['incomplete_results'] == False:
                json_parsed = json.loads(content)['items']
                write_csv('data/(test)savedata20170731.csv', json_parsed,
                          'id', 'name', 'full_name',
                          'owner', 'private', 'html_url',
                          'description', 'fork', 'url',
                          'forks_url', 'keys_url', 'keys_url',
                          'collaborators_url', 'teams_url', 'hooks_url',
                          'issue_events_url', 'events_url', 'assignees_url',
                          'branches_url', 'tags_url', 'blobs_url',
                          'git_tags_url', 'git_refs_url', 'trees_url',
                          'statuses_url', 'languages_url', 'stargazers_url',
                          'contributors_url', 'subscribers_url', 'subscription_url',
                          'commits_url', 'git_commits_url', 'comments_url',
                          'issue_comment_url', 'contents_url', 'compare_url',
                          'merges_url', 'archive_url', 'downloads_url',
                          'issues_url', 'pulls_url', 'milestones_url',
                          'notifications_url', 'labels_url', 'releases_url',
                          'deployments_url', 'created_at', 'updated_at',
                          'pushed_at', 'git_url', 'ssh_url',
                          'clone_url', 'svn_url', 'homepage',
                          'size', 'stargazers_count', 'watchers_count',
                          'language', 'has_issues', 'has_projects',
                          'has_downloads', 'has_wiki', 'has_pages',
                          'forks_count', 'mirror_url', 'open_issues_count',
                          'forks', 'open_issues', 'watchers',
                          'default_branch', 'permissions', 'score')
                next = find_link(response,'next')
                count_last += 1
            else:
                print 'incomplete results'
        except KeyError:
            sleep(2)

count=6602
while count>86:
    url = 'https://api.github.com/search/repositories?q=stars:'+str(count)+'&per_page=100&sort=stars'
    print url
    try:
        response, content = request(url)
        if json.loads(content)['incomplete_results'] == False:
            print 'Repository count: '+str(json.loads(content)['total_count'])
            json_parsed = json.loads(content)['items']
            write_csv('data/(test)savedata20170731.csv',json_parsed,
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
                      'default_branch','permissions','score')
            try:
                next = find_link(response,'next')
                last = find_link(response,'last')
                next_page(next,last,url)
            except KeyError:
                pass
        else:
            print 'incomplete result'
        count -= 1
    except KeyError:
        sleep(2)

# url = 'https://api.github.com/search/repositories?q=created:>2015-01-01+stars:>1&per_page=100&sort=stars'
# print url
# response, content = request(url)
# json_parsed = json_parse(content)
# write_csv('forkcount.csv',json_parsed,'full_name','forks_count')
# next = find_link(response)
# next_page(next)


