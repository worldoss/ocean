#-*- coding: utf-8 -*-
import httplib2
import json
import base64
import csv
from time import sleep

class NotincompleteError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

class NoresultError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

def request(url):
    http = httplib2.Http()
    id = 'rlrlaa123'
    pw = 'ehehdd009'
    auth = base64.encodestring(id + ':' + pw)
    return http.request(url,'GET',headers={ 'Authorization' : 'Basic ' + auth})

# 언어별 1000번째 저장소 star수
lang_thousand={
    'ActionScript':10,
    'C':428,
    # 'CSharp':227,
    # 'CPP':421,
    # 'Clojure':64,
    'CoffeeScript':63,
    'CSS':262,
    'Go':475,
    'Haskell':35,
    'HTML':322,
    # 'Java':1270,
    'Javascript':2908,
    # 'Lua':36,
    # 'Matlab':9,
    # 'Objective-C':716,
    # 'Perl':32,
    # 'PHP':458,
    # 'Python':1012,
    # 'R':30,
    # 'Ruby':600,
    # 'Scala':75,
    # 'Shell':215,
    # 'Swift':359,
    #  'TeX':15,
    #  'Vim-script':59
}

lang_items=lang_thousand.items()
for lang in lang_items:
    count=lang[1]-1
    while count>5:
        url = 'https://api.github.com/search/repositories?q=stars:'+str(count)+'+language:"'+lang[0]+'"&per_page=100'
        print url
        try:
            response, content = request(url)
            json_parsed =  json.loads(content)['total_count']
            if json.loads(content)['incomplete_results'] == False:
                if int(json_parsed) != 0:
                    print count, json_parsed
                    with open('data/(donghyun)star_per_repository_language.csv','a') as csvfile:
                        writer= csv.writer(csvfile)
                        writer.writerow([lang[0]]+[str(count)]+[json_parsed])
                        count-=1
                else:
                    raise NoresultError('No results')
            else:
                raise NotincompleteError('Incomplete results, try again')
        except NotincompleteError as e:
            print e
        except NoresultError as e:
            count-=1
            print e
        except KeyError:
            sleep(1)