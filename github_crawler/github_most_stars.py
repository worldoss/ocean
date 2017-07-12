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

# Start requesting repositories
url = 'https://api.github.com/search/repositories?per_page=100&q=stars:>1'
response, content = request(url)
repositories=json.loads(content)

p1=re.compile('([\d]+)>; rel="next"')
next = p1.findall(response['link'])
p2=re.compile('([\d]+)>; rel="last"')
last = p2.findall(response['link'])
for repo in repositories['items']:
    result.append([repo['full_name'], repo['stargazers_count']])

for page in range(int(last[0])-1):
    page_url = url + '&page=' + next[0]
    print page_url
    response, content = request(page_url)
    page_repositories = json.loads(content)
    for page_repo in page_repositories['items']:
        result.append([page_repo['full_name'],page_repo['stargazers_count']])
    p1 = re.compile('([\d]+)>; rel="next"')
    next = p1.findall(response['link'])
    with open('top_star_repository.txt', 'a') as f:
        for data in result:
            f.write(data[0] + ': %d\n' % data[1])
    result = []
