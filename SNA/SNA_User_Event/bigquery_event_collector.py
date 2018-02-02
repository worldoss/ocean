# -*- coding: utf-8 -*-

## Bigquery credential file needed!
## Reference: https://cloud.google.com/bigquery/docs/authentication/service-account-file

import requests
import os
import csv
import collections
import networkx as nx
from shutil import copyfile, copytree

from google.cloud import bigquery

class UserDoesNotExistError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg
class NotFoundError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

class EventAnalysis():
    def __init__(self,folder_name):
        # BigQuery API 인증키
        service_account = 'Github-SNA-6cf7f22bd6fb.json'
        # BigQuery API 인증요청
        self.client = bigquery.Client.from_service_account_json(service_account)
        # 쿼리문 (다음 쿼리문이 유효한 테이블이 있어야함)
        self.QUERY = """
        SELECT
          repo_name,
          event_type,
          pullrequest_comment_actor,
          pullreqeust_actor,
          commit_comment_actor,
          commit_actor,
          issue_comment_actor,
          issue_actor
        FROM
          `github-sna.SNA.15_17_refined_eventactor`
        WHERE
          repo_name = """

        self.REPOSITORY = []
        self.folder_name = folder_name

        # 봇 리스트
        self.BOT_LIST = []
        # 봇 리스트 추가
        with open('bot_list.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                self.BOT_LIST.append(row[0])
                self.BOT_LIST.append(int(row[0]))
            self.BOT_LIST = list(set(self.BOT_LIST))
    # 저장소 리스트 추가
    def getRepositories(self,get_repository_from):
        with open(get_repository_from, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for i in reader:
                self.REPOSITORY.append(i[0])

    def collectEvent(self,repo,id,pw):
        repo_name = repo.replace('/',':')
        # Create Directory
        if not os.path.exists('SNA_User_Event_'+self.folder_name+'/'+repo_name):
            os.makedirs('SNA_User_Event_'+self.folder_name+'/'+repo_name)
        print (repo_name)
        # Create csv file
        with open('SNA_User_Event_'+self.folder_name+'/'+repo_name+'/'+repo_name+'.csv', 'a') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(
                ['repo_name', 'event_type', 'pullrequest_comment_actor', 'pullrequest_actor', 'commit_comment_actor',
                 'commit_actor', 'issue_comment_actor', 'issue_actor','weight'])
            # Iterate Queries
            # for query in QUERY:
            print ("Query Sent...")
            # Send Query
            query_job = self.client.query(self.QUERY+"'"+repo+"'") # LIMIT 10 should be removed...
            result = query_job.result()

            data = []
            count_list = {
                'PullRequestReviewCommentEvent':[],
                'CommitCommentEvent':[],
                'IssueCommentEvent':[],
            }
            counter_list = {}
            for row in result:
                if row[0] in self.BOT_LIST or row[1] in self.BOT_LIST or row[2] in self.BOT_LIST or row[3] in self.BOT_LIST or row[4] in self.BOT_LIST or row[5] in self.BOT_LIST or row[6] in self.BOT_LIST or row[7] in self.BOT_LIST:
                    continue
                if row[1] == 'PullRequestReviewCommentEvent' or row[1] == 'PullRequestReviewComment':
                    data.append([row[0],row[1],row[2],row[3],0,0,0,0])
                    count_list['PullRequestReviewCommentEvent'].append((row[2], row[3]))
                elif row[1] == 'CommitCommentEvent' or row[1] == 'CommitComment':
                    data.append([row[0],row[1],0,0,row[4],str(row[5]).replace('"',''),0,0])
                    count_list['CommitCommentEvent'].append((row[4],row[5].replace('"','')))
                elif row[1] == 'IssueCommentEvent' or row[1] == 'IssueComment':
                    data.append([row[0],row[1],0,0,0,0,row[6],row[7]])
                    count_list['IssueCommentEvent'].append((row[6], row[7]))

            for count in count_list:
                counter_list[count] = collections.Counter(count_list[count])

            for event in counter_list:
                for row in counter_list[event]:
                    if event == 'PullRequestReviewCommentEvent' or event == 'PullRequestReviewComment':
                        writer.writerow([repo,event,row[0],row[1],0,0,0,0,counter_list[event][row]])
                    elif event == 'CommitCommentEvent' or event == 'CommitComment':
                        commit_user_id = self.collectCommitUser(row[1],repo,id,pw)
                        writer.writerow([repo,event,0,0,row[0],commit_user_id,0,0,counter_list[event][row]])
                    elif event == 'IssueCommentEvent' or event == 'IssueComment':
                        writer.writerow([repo,event,0,0,0,0,row[0],row[1],counter_list[event][row]])
        print ('Query Finished...\n')
    def snaAnalysis(self,repo):
        repo_name = repo.replace('/',':')
        sna = {
            'PullRequestReviewCommentEvent': {
                'node_list':[],
                'edge_list':[],
                'density':0
            },
            'CommitCommentEvent': {
                'node_list':[],
                'edge_list':[],
                'density':0
            },
            'IssueCommentEvent': {
                'node_list':[],
                'edge_list':[],
                'density':0
            },
        }
        with open('SNA_User_Event_'+self.folder_name+'/'+repo_name+'/'+repo_name+'.csv','r',encoding='utf-8') as csvfile:
            reader = (csv.reader(csvfile))
            for row in reader:
                if row[1] == 'PullRequestReviewCommentEvent':
                    sna['PullRequestReviewCommentEvent']['node_list'].append(row[2])
                    sna['PullRequestReviewCommentEvent']['node_list'].append(row[3])
                    sna['PullRequestReviewCommentEvent']['edge_list'].append((row[2],row[3],int(row[-1])))
                elif row[1] == 'CommitCommentEvent':
                    sna['CommitCommentEvent']['node_list'].append(row[4])
                    sna['CommitCommentEvent']['node_list'].append(row[5])
                    sna['CommitCommentEvent']['edge_list'].append((row[4], row[5], int(row[-1])))
                elif row[1] == 'IssueCommentEvent':
                    sna['IssueCommentEvent']['node_list'].append(row[6])
                    sna['IssueCommentEvent']['node_list'].append(row[7])
                    sna['IssueCommentEvent']['edge_list'].append((row[6], row[7], int(row[-1])))

        for event in sna:
            print ('START '+repo_name+' '+event+'...')
            node_list = sna[event]['node_list']
            edge_list = sna[event]['edge_list']

            node_list = list(set(node_list))

            G = nx.DiGraph()
            G.add_nodes_from(node_list)
            G.add_weighted_edges_from(edge_list)
            print(nx.info(G))

            # print(edge_list)
            # nx.draw_networkx(G)
            # plt.show()
            try:
                user_indegree = nx.in_degree_centrality(G)
                print('FINISHED INDEGREE CENTRALITY...')
                user_outdegree = nx.out_degree_centrality(G)
                print('FINISHED OUTDEGREE CENTRALITY...')
                user_closeness = nx.closeness_centrality(G)
                print('FINISHED CLOSENESS CENTRALITY...')
                user_betweeness = nx.betweenness_centrality(G)
                print('FINISHED BETWEENESS CENTRALITY...')
                user_eigenvector = {}

                try:
                    user_eigenvector = nx.eigenvector_centrality_numpy(G)
                except:
                    print('EIGENVECTOR INVALID')
                    for i in node_list:
                        user_eigenvector[i] = 0
                print('FINISHED EIGENVECTOR CENTRALITY...')

                with open('SNA_User_Event_'+self.folder_name+'/'+repo_name + '/SNA_' + event + '_' + repo_name + '.csv', 'w', encoding='utf-8') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['user', 'indegree_centrality', 'outdegree_centrality', 'closeness_centrality', 'betweenness_centrality',
                                     'eigenvector_centrality'])

                    for user in node_list:
                        writer.writerow([
                            user,
                            user_indegree[user],
                            user_outdegree[user],
                            user_closeness[user],
                            user_betweeness[user],
                            user_eigenvector[user]
                        ])

                print ('START DENSITY...')
                if event == 'PullRequestReviewCommentEvent':
                    sna[event]['density'] = nx.density(G)
                elif event == 'CommitCommentEvent':
                    sna[event]['density'] = nx.density(G)
                elif event == 'IssueCommentEvent':
                    sna[event]['density'] = nx.density(G)
                print(event+' Density: '+str(sna[event]['density']))
            except ZeroDivisionError:
                pass
            except UnicodeEncodeError:
                print('unicode error')
    def typeCount(self,repo):
        print (repo+' Type Count Starts...')
        repo_name = repo.replace('/',':')
        user = []
        user_type = {}
        with open('SNA_User_Event_'+self.folder_name+'/'+repo_name+'/'+repo_name+'.csv', 'r',encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[1] == 'IssueCommentEvent' or row[1] == 'IssueCommentEvent':
                    user.append(row[6])
                    user.append(row[7])
                elif row[1] == 'PullRequestReviewCommentEvent' or row[1] == 'PullRequestReviewCommentEvent':
                    user.append(row[2])
                    user.append(row[3])
                elif row[1] == 'CommitCommentEvent' or row[1] == 'CommitCommentEvent':
                    user.append(row[4])
                    user.append(row[5])

            user = list(set(user))

            for u in user:
                user_type[u]={
                    'IssueEvent':0,
                    'IssueCommentEvent':0,
                    'PullRequestEvent':0,
                    'PullRequestCommentEvent':0,
                    'CommitEvent':0,
                    'CommitCommentEvent':0,
                }
        with open('SNA_User_Event_'+self.folder_name+'/'+repo_name+'/'+repo_name+'.csv', 'r',encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                if row[1] == 'IssueCommentEvent':
                    for u in user:
                        if u == row[6]:
                            user_type[u]['IssueCommentEvent']+=1 # row[8]
                    for u in user:
                        if u == row[7]:
                            user_type[u]['IssueEvent']+=1
                elif row[1] == 'PullRequestReviewCommentEvent':
                    for u in user:
                        if u == row[2]:
                            user_type[u]['PullRequestCommentEvent']+=1
                    for u in user:
                        if u == row[3]:
                            user_type[u]['PullRequestEvent']+=1
                elif row[1] == 'CommitCommentEvent':
                    for u in user:
                        if u == row[4]:
                            user_type[u]['CommitCommentEvent']+=1
                    for u in user:
                        if u == row[5]:
                            user_type[u]['CommitEvent']+=1

        with open('SNA_User_Event_'+self.folder_name+'/'+repo_name+'/'+repo_name+'_TypeCount'+'.csv','w',encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile,fieldnames=['user','IssueEvent','IssueCommentEvent','CommitEvent','CommitCommentEvent','PullRequestEvent','PullRequestCommentEvent'])
            writer.writeheader()
            for user in user_type:
                user_type[user]['user']=user
                writer.writerow(user_type[user])
    def userCategorize(self,repo):
        # 'Issue','IssueComment','Commit','CommitComment','PullRequest','PullRequestComment',
        print (repo+' User Categorize Starts...')
        repo_name = repo.replace('/',':')
        user_type = {}
        with open('SNA_User_Event_'+self.folder_name+'/'+repo_name+'/'+repo_name+'_TypeCount.csv','r',encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:

                issue = row[1]
                issuecomment = row[2]
                commit = row[3]
                commitcomment = row[4]
                pullrequest = row[5]
                pullrequestcomment = row[6]

                if len(str(row[1])) > 1:
                    issue = '1'
                if len(str(row[2])) > 1:
                    issuecomment = '1'
                if len(str(row[3])) > 1:
                    commit = '1'
                if len(str(row[4])) > 1:
                    commitcomment = '1'
                if len(str(row[5])) > 1:
                    pullrequest = '1'
                if len(str(row[6])) > 1:
                    pullrequestcomment = '1'
                if str(row[1]) != '0':
                    issue = '1'
                if str(row[2]) != '0':
                    issuecomment = '1'
                if str(row[3]) != '0':
                    commit = '1'
                if str(row[4]) != '0':
                    commitcomment = '1'
                if str(row[5]) != '0':
                    pullrequest = '1'
                if str(row[6]) != '0':
                    pullrequestcomment = '1'

                countedevents = issue+issuecomment+commit+commitcomment+pullrequest+pullrequestcomment

                case = []
                for i in range(64):
                    case.append('{0:06b}'.format(i))
                for binarytype in case:
                    if countedevents == binarytype:
                        user_type[row[0]]='Type ' + str(int(binarytype,2))

        with open('SNA_User_Event_'+self.folder_name+'/'+repo_name+'/'+repo_name+'_Categorized.csv','w',encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['user','type'])
            for user in user_type:
                writer.writerow([user,user_type[user]])
    def categorizedUserCount(self):
        with open('SNA_User_Event_'+self.folder_name+'/'+'RepoCategorized_'+self.folder_name+'.csv', 'w',encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=['Repository'] + ['Type '+str(i) for i in range(1, 64)])
            writer.writeheader()
            for repo in self.REPOSITORY:
                repo_name = repo.replace('/',':')
                type_dict = {
                    'Type '+str(i):0 for i in range(1,64)
                }
                type_dict['Repository'] = repo_name
                print (repo+' Categorized User Count Starts...')
                type = []
                with open('SNA_User_Event_'+self.folder_name+'/'+repo_name+'/'+repo_name+'_Categorized.csv','r',encoding='utf-8') as csvfile:
                    reader = csv.reader(csvfile)
                    next(reader)
                    for row in reader:
                        type.append(row[1])
                    counter = collections.Counter(type)
                    for i in counter:
                        type_dict[i] = counter[i]
                # print (type_dict)
                writer.writerow(type_dict)
    def Request(self,url,github_id,github_pw):
        id = github_id
        pw = github_pw
        return requests.get(url,auth=(id,pw))
    def collectCommitUser(self,commit_id,repo_name,id,pw):
        try:
            # time.sleep(1.5)
            url_commit_id = 'https://api.github.com/repos/'+repo_name+'/commits/'+str(commit_id)
            print (url_commit_id)
            content = self.Request(url_commit_id,id,pw).json()
            if content['committer'] != None:
                user_login = content['committer']['login']
                url_commit_user = 'https://api.github.com/users/' + str(user_login)
                print (url_commit_user)
                url_limit = 'https://api.github.com/rate_limit'
                print(self.Request(url_limit,id,pw).json()['rate']['remaining'])
                content = self.Request(url_commit_user,id,pw).json()
                return content['id']
            # elif content['message'] == 'Not Found':
            #     raise NotFoundError
            else:
                raise UserDoesNotExistError('User Does Not Exist')
        except UserDoesNotExistError as e:
            print (e)
            user_name = content['commit']['committer']['name']
            return user_name
        except KeyError as e:
            print (e)
            return 'Not Found'
    def snaDensity(self):
        with open('SNA_User_Event_'+self.folder_name+'/'+'RepoDensity_'+self.folder_name+'.csv', 'w',encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['repo_name', 'PullRequestDensity', 'CommitDensity', 'IssueDensity', 'TotalDensity'])

            for repo in self.REPOSITORY:
                repo_name = repo.replace('/', ':')
                sna = {
                    'PullRequestReviewCommentEvent': {
                        'node_list': [],
                        'edge_list': [],
                        'density': 0
                    },
                    'CommitCommentEvent': {
                        'node_list': [],
                        'edge_list': [],
                        'density': 0
                    },
                    'IssueCommentEvent': {
                        'node_list': [],
                        'edge_list': [],
                        'density': 0
                    },
                    'TotalEvent': {
                        'node_list': [],
                        'edge_list': [],
                        'density': 0,
                    }
                }
                with open('SNA_User_Event_'+self.folder_name+'/'+repo_name + '/' + repo_name + '.csv', 'r', encoding='utf-8') as csvfile:
                    reader = (csv.reader(csvfile))
                    next(reader)
                    for row in reader:
                        if row[1] == 'PullRequestReviewCommentEvent' or row[1] == 'PullRequestReviewCommentEvent':
                            sna['PullRequestReviewCommentEvent']['node_list'].append(row[2])
                            sna['PullRequestReviewCommentEvent']['node_list'].append(row[3])
                            sna['PullRequestReviewCommentEvent']['edge_list'].append((row[2], row[3], int(row[-1])))
                            sna['TotalEvent']['node_list'].append(row[2])
                            sna['TotalEvent']['node_list'].append(row[3])
                            sna['TotalEvent']['edge_list'].append((row[2],row[3],int(row[-1])))
                        elif row[1] == 'CommitCommentEvent' or row[1] == 'CommitCommentEvent':
                            sna['CommitCommentEvent']['node_list'].append(row[4])
                            sna['CommitCommentEvent']['node_list'].append(row[5])
                            sna['CommitCommentEvent']['edge_list'].append((row[4], row[5], int(row[-1])))
                            sna['TotalEvent']['node_list'].append(row[4])
                            sna['TotalEvent']['node_list'].append(row[5])
                            sna['TotalEvent']['edge_list'].append((row[4], row[5], int(row[-1])))
                        elif row[1] == 'IssueCommentEvent' or row[1] == 'IssueCommentEvent':
                            sna['IssueCommentEvent']['node_list'].append(row[6])
                            sna['IssueCommentEvent']['node_list'].append(row[7])
                            sna['IssueCommentEvent']['edge_list'].append((row[6], row[7], int(row[-1])))
                            sna['TotalEvent']['node_list'].append(row[6])
                            sna['TotalEvent']['node_list'].append(row[7])
                            sna['TotalEvent']['edge_list'].append((row[6], row[7], int(row[-1])))
                # Event Density
                for event in sna:
                    print('START ' + repo_name + ' ' + event + '...')
                    node_list = sna[event]['node_list']
                    edge_list = sna[event]['edge_list']

                    node_list = list(set(node_list))

                    G = nx.DiGraph()
                    G.add_nodes_from(node_list)
                    G.add_weighted_edges_from(edge_list)

                    # print(edge_list)
                    # nx.draw_networkx(G)
                    # plt.show()

                    print('START DENSITY...')
                    if event == 'PullRequestReviewCommentEvent' or event == 'PullRequestReviewCommentEvent':
                        sna[event]['density'] = nx.density(G)
                        print ('PullRequest Density: ' + str(sna['PullRequestReviewCommentEvent']['density']))
                    elif event == 'CommitCommentEvent' or event == 'CommitCommentEvent':
                        sna[event]['density'] = nx.density(G)
                        print ('Commit Density: ' + str(sna['CommitCommentEvent']['density']))
                    elif event == 'IssueCommentEvent' or event == 'IssueCommentEvent':
                        sna[event]['density'] = nx.density(G)
                        print('Issue Density: ' + str(sna['IssueCommentEvent']['density']))

                # Total Event Density
                node_list = sna['TotalEvent']['node_list']
                edge_list = sna['TotalEvent']['edge_list']

                node_list = list(set(node_list))

                T = nx.DiGraph()
                T.add_nodes_from(node_list)
                T.add_weighted_edges_from(edge_list)

                sna['TotalEvent']['density'] = nx.density(T)
                print ('Total Density: '+ str(sna['TotalEvent']['density']))

                writer.writerow([repo_name,sna['PullRequestReviewCommentEvent']['density'],sna['CommitCommentEvent']['density'],sna['IssueCommentEvent']['density'],sna['TotalEvent']['density']])
    def countRatio(self):
        with open('SNA_User_Event_'+self.folder_name+'/'+'Repocategorized_ratio_'+self.folder_name+'.csv','w',encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Repository']+['Type '+str(i) for i in range(1, 64)])
            with open('SNA_User_Event_'+self.folder_name+'/'+'RepoCategorized_'+self.folder_name+'.csv','r',encoding='utf-8') as csvfile2:
                reader = csv.reader(csvfile2)
                next(reader)
                for row in reader:
                    total = 0.0
                    ratio = []
                    for type in row[1:]:
                        # print (type)
                        total += float(type)
                    for type in row[1:]:
                        if total != 0:
                            ratio.append(round(float(type)/total*100,1))
                        else:
                            ratio.append(0)
                    writer.writerow([row[0]]+ratio)
    def snaMaxAvg(self):
        with open('SNA_User_Event_'+self.folder_name+'/'+'snaMaxAvg_'+self.folder_name+'.csv','w',encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile,fieldnames=[
                'Repository',
                'commit_in_max',
                'commit_in_avg',
                'commit_out_max',
                'commit_out_avg',
                'pullre_in_max',
                'pullre_in_avg',
                'pullre_out_max',
                'pullre_out_avg',
                'issue_in_max',
                'issue_in_avg',
                'issue_out_max',
                'issue_out_avg',
            ])
            writer.writeheader()

            for repo in self.REPOSITORY:
                repo_name = repo.replace('/',':')
                snaMaxAvg = {
                    'Repository':repo,
                    'commit_in_max':0.0,
                    'commit_in_avg':0.0,
                    'commit_out_max':0.0,
                    'commit_out_avg':0.0,
                    'pullre_in_max':0.0,
                    'pullre_in_avg':0.0,
                    'pullre_out_max':0.0,
                    'pullre_out_avg':0.0,
                    'issue_in_max':0.0,
                    'issue_in_avg':0.0,
                    'issue_out_max':0.0,
                    'issue_out_avg':0.0,
                }
                for event in ['IssueCommentEvent','CommitCommentEvent','PullRequestReviewCommentEvent']:
                    if not os.path.exists('SNA_User_Event_'+self.folder_name+'/'+repo_name+'/SNA_'+event+'_'+repo_name+'.csv'):
                        print ('no repo')
                        with open('SNA_User_Event_'+self.folder_name+'/'+repo_name+'/SNA_'+event+'_'+repo_name+'.csv','w',encoding='utf-8') as csvfile3:
                            writer3 = csv.writer(csvfile3)
                            writer3.writerow(['user','indegree_centrality','outdegree_centrality','closeness_centrality','betweenness_centrality','eigenvector_centrality'])
                    with open('SNA_User_Event_'+self.folder_name+'/'+repo_name+'/SNA_'+event+'_'+repo_name+'.csv','r',encoding='utf-8') as csvfile2:
                        print ('Start '+repo_name)
                        reader2 = csv.reader(csvfile2)
                        indegree = []
                        outdegree = []
                        next(reader2)

                        for row in reader2:
                            indegree.append(float(row[1]))
                            outdegree.append(float(row[2]))
                        if event == 'IssueCommentEvent':
                            if len(indegree) == 0:
                                snaMaxAvg['issue_in_avg'] = 0.0
                                snaMaxAvg['issue_in_max'] = 0.0
                            if len(outdegree) == 0:
                                snaMaxAvg['issue_out_avg'] = 0.0
                                snaMaxAvg['issue_out_max'] = 0.0
                            else:
                                snaMaxAvg['issue_out_avg'] = sum(outdegree)/len(outdegree)
                                snaMaxAvg['issue_out_max'] = max(outdegree)
                                snaMaxAvg['issue_in_avg'] = sum(indegree) / len(indegree)
                                snaMaxAvg['issue_in_max'] = max(indegree)
                        elif event == 'CommitCommentEvent':
                            if len(indegree) == 0:
                                snaMaxAvg['commit_in_avg'] = 0.0
                                snaMaxAvg['commit_in_max'] = 0.0
                            if len(outdegree) == 0:
                                snaMaxAvg['commit_out_avg'] = 0.0
                                snaMaxAvg['commit_out_max'] = 0.0
                            else:
                                snaMaxAvg['commit_out_avg'] = sum(outdegree)/len(outdegree)
                                snaMaxAvg['commit_out_max'] = max(outdegree)
                                snaMaxAvg['commit_in_avg'] = sum(indegree) / len(indegree)
                                snaMaxAvg['commit_in_max'] = max(indegree)
                        elif event == 'PullRequestReviewCommentEvent':
                            if len(indegree) == 0:
                                snaMaxAvg['pullre_in_avg'] = 0.0
                                snaMaxAvg['pullre_in_max'] = 0.0
                            if len(outdegree) == 0:
                                snaMaxAvg['pullre_out_avg'] = 0.0
                                snaMaxAvg['pullre_out_max'] = 0.0
                            else:
                                snaMaxAvg['pullre_out_avg'] = sum(outdegree)/len(outdegree)
                                snaMaxAvg['pullre_out_max'] = max(outdegree)
                                snaMaxAvg['pullre_in_avg'] = sum(indegree) / len(indegree)
                                snaMaxAvg['pullre_in_max'] = max(indegree)
                writer.writerow(snaMaxAvg)