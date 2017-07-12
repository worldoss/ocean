import httplib2
import json
import base64
import re

result = []

http = httplib2.Http()

# Request function
def request(url):
    auth = base64.encodestring('rlrlaa123' + ':' + 'ehehdd009')
    return http.request(url,'GET',headers={ 'Authorization' : 'Basic ' + auth})
# Count and Print how many stars per repository
def count_star(repositories):
    for repo in repositories:
        response, content = request(repo['stargazers_url'] + '?per_page=100')
        stargazers_url = json.loads(content)

        if 'link' in response:
            count = 0
            p1 = re.compile('([\d]+)>; rel="next"')
            next = p1.findall(response['link'])
            p2 = re.compile('([\d]+)>; rel="last"')
            last = p2.findall(response['link'])
            count += len(stargazers_url)

            for i in range(int(last[0]) - 1):
                url = repo['stargazers_url'] + '?per_page=100' + '&page=' + next[0]
                response, content = request(url)
                star_users = json.loads(content)
                count += len(star_users)
                p1 = re.compile('([\d]+)>; rel="next"')
                next = p1.findall(response['link'])
            print repo['full_name']
            print count
            result.append([repo['full_name'],count])

        else:
            count = 0
            url = repo['stargazers_url'] + '?per_page=100'
            response, content = request(url)
            star_users = json.loads(content)
            count += len(star_users)
            print repo['full_name']
            print count
            result.append([repo['full_name'],count])

# Start requesting repositories
url = 'https://api.github.com/repositories?per_page=100&since=0'
response, content = request(url)
repositories=json.loads(content)
# Count first 100 repositories' stars
count_star(repositories)

p1 = re.compile('([\d]+)>; rel="next"')
next = p1.findall(response['link'])

while True:
    try:
        # Go to next 100 repositories
        print 'Enter While'
        pageurl = url+'?per_page=100'+'&since='+next[0]
        response, content = request(pageurl)
        repositories = json.loads(content)
        print response['link']
        # Count next 100 repositories' stars
        count_star(repositories)
        p1 = re.compile('([\d]+)>; rel="next"')
        next = p1.findall(response['link'])
    except KeyboardInterrupt as e:
        print 'Keyboard Interrupt Error'
    except 'X-RateLimit-Remaining' == 1 in response as e:
        print 'Limit-rate remain 1'
    except 'link' not in response as e:
        print 'No link error'
    # Add repositroy full_name and stars to result.txt file...
    finally:
        print 'Input data'
        with open('result.txt', 'a') as f:
            for data in result:
                f.write(data[0] + ': %d\n' % data[1])
        result = []