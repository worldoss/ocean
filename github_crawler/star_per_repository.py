import httplib2
import json
import base64
import csv
import time

def request(url):
    http = httplib2.Http()
    id = 'rlrlaa123'
    pw = 'ehehdd009'
    auth = base64.encodestring(id + ':' + pw)
    return http.request(url,'GET',headers={ 'Authorization' : 'Basic ' + auth})

def json_count(data):
    return json.loads(data)['total_count']

count=1
while count<=6587:
    url = 'https://api.github.com/search/repositories?q=stars:'+str(count)+'&per_page=100'
    response, content = request(url)
    if json.loads(content)['incomplete_resuts'] == False:
        json_parsed = json_count(content)
        print count, json_parsed
        if int(json_parsed) != 0:
            with open('data/star_per_repository.csv','a') as csvfile:
                writer= csv.writer(csvfile)
                writer.writerow([str(count)]+[json_parsed])
                count+=1
    else:
        pass
    time.sleep(2)
