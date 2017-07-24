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

def choose_option():
    while 1:
        option = input("Select option (1.type url, 2.use default url)\nOption: ")
        if option == 1:
            return raw_input("Type url: ")
        elif option == 2:
            return 'https://api.github.com/search/repositories?q=stars:5&per_page=100'
        else:
            print "Wrong option, choose between given options"

def json_parse(data):
    return json.loads(data)['items']

def json_count(data):
    return json.loads(data)['total_count']

def write_csv(filename,json_data,*args):
    with open(filename,'a') as csvfile:
        fieldnames = []
        fieldnames_dict = {}
        for field in args:
            fieldnames.append(field)
        writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
        # writer.writeheader()
        for data in json_data:
            for field in args:
                fieldnames_dict[field]=data[field]
            writer.writerow(fieldnames_dict)
            fieldnames_dict = {}

def write_count_csv(filename,json_data,date):
    with open(filename,'a') as csvfile:
        writer = csv.writer(csvfile)
        # writer.writeheader()
        writer.writerow([date,json_data])

def find_link(response):
    return re.compile('([0-9]+)>; rel="next"').findall(response['link'])

def next_page(next):
    while True:
        try:
            response, content = request(url + '&page=' + str(next[0]))
            print response['link']
            json_parsed = json_parse(content)
            next = find_link(response)
        except IndexError as e:
            print 'Response link ' + str(e)
            print 'Finished'
            break
        except KeyError as e:
            break
        finally:
            write_csv('./forkcount.csv', json_parsed, 'full_name', 'forks_count')


# url = 'https://api.github.com/search/repositories?q=forks:>1&sort=forks&per_page=100'
# response, content = request(url)
# json_parsed = json_parse(content)
# write_csv('forkcount.csv',json_parsed,'full_name','forks_count')
# next = find_link(response)
# next_page(next)

#str(1).zfill(2)

def countingByDate():
    url = 'https://api.github.com/search/repositories?q=created:' + str(year) + '-' + str(month).zfill(2) + '-' + str(
        day).zfill(2) + '&per_page=100'
    print url
    response, content = request(url)
    json_parsed = json_count(content)
    date = str(year) + '-' + str(month).zfill(2) + '-' + str(day).zfill(2)
    write_count_csv('createdcount.csv', json_parsed, date)

thirtyone = [1,3,5,7,8,10,12]
thirty = [4,6,9,11]
twentyeight = [2]
year=2015
for year_loop in range(3):
    for month in range(12):
        if month in thirtyone:
            for day in range(1,32):
                countingByDate()
        if month in thirty:
            for day in range(1,31):
                countingByDate()
        if month in twentyeight:
            for day in range(1,29):
                countingByDate()
        sleep(2)
    year+=1

# 끝나고 2016년 2월 29일 추가해줘야함