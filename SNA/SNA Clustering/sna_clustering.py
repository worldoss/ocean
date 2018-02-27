# -*- coding: utf-8 -*-

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import csv
import community
import operator
from nltk.corpus import stopwords

class SNACluster():
    def __init__(self,folder_name,classification_translation,new_repo_topic_data):
        self.folder_name = folder_name
        self.classification = {
            'System SW': [],
            'Application SW': [],
        }
        self.new_repo_topic_data = new_repo_topic_data
        with open(classification_translation, 'r', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)
            for row in reader:
                try:
                    if '\t' in row[0] or '\t' in row[1]:
                        self.classification['System SW'].append(row[0].replace('\t',''))
                        self.classification['Application SW'].append(row[1].replace('\t',''))
                    else:
                        self.classification['System SW'].append(row[0])
                        self.classification['Application SW'].append(row[1])
                except IndexError:
                    pass
        remove_text_list = [',', '.', '/', "'", '"', '(', ')', '{', '}', '[', ']']
        stop_words = set(stopwords.words('english'))
        self.result = {}
        for i in self.classification:
            self.result[i] = []
        for i in self.classification:
            for index, j in enumerate(self.classification[i]):
                for k in remove_text_list:
                    if k in j:
                        self.classification[i][index] = j.replace(k, ' ')
            print (self.classification[i])
            for j in self.classification[i]:
                for k in j.split(' '):
                    self.result[i].append(k.lower())

            self.result[i] = list(set(self.result[i]))
            if '' in self.result[i]:
                self.result[i].remove('')
            for j in stop_words:
                if j in self.result[i]:
                    self.result[i].remove(j)
    def create_graph(self):
        data = pd.read_csv(self.new_repo_topic_data, error_bad_lines=False, header=None,
                           sep=",", delimiter='\n')  # pandas 라이브러리를 이용해서 SNA 분석 csv 파일 불러오기
        # Creating node list
        node = []
        for i in data.values:
            for j in i[0].split(',')[1:]:
                node.append(j)

        node = list(set(node))

        # Creating edge list
        self.edges = []

        for i in data.values:
            l = i[0].split(',')[1:]
            for j in range(len(l)):
                for k in range(j + 1, len(l)):
                    self.edges.append((l[j], l[k]))

        self.G = nx.Graph()
        self.G.add_nodes_from(node)
        self.G.add_edges_from(self.edges)

        print (nx.number_of_nodes(self.G))
        print (nx.number_of_edges(self.G))
    def match_edgelist(self,row):
        cluster = row[1:]
        edges = []
        # print cluster
        for index,i in enumerate(self.edges):
            for j in cluster:
                if i[0] == j:
                    for k in cluster:
                        if i[1] == k:
                            edges.append(i)
                            continue
                if i[1] == j:
                    for k in cluster:
                        if i[0] == k:
                            edges.append(i)
                            continue
        return cluster, edges
    def centrality(self):
        with open(self.folder_name+'/community.csv','rU') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                cluster, edges = self.match_edgelist(row)
                edges = list(set(edges))

                C = nx.Graph()
                C.add_nodes_from(cluster)
                C.add_edges_from(edges)

                node_count=nx.number_of_nodes(C)
                edge_count=nx.number_of_edges(C)

                print (node_count, edge_count)

                cent = self.degree_centrality_custom(C)

                print (cent)

                with open(self.folder_name+'/centrality.csv','a') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['Community '+row[0],'Node: '+str(node_count),'Edge: '+str(edge_count)])
                    for i,j in cent.items():
                        writer.writerow([i,j])
                print ('Finished Community '+row[0])
    def clustering(self,resolution):
        partition = community.best_partition(self.G,resolution=resolution)
        with open(self.folder_name+'/community.csv','a') as csvfile:
            writer = csv.writer(csvfile)
            for community_num in set(partition.values()):
                print ("Community", community_num)
                members = list_nodes = [nodes for nodes in partition.keys() if partition[nodes] == community_num]
                print (members)
                writer.writerow([community_num]+members)

        # #drawing
        # size = float(len(set(partition.values())))
        # pos = nx.spring_layout(self.G)
        # count = 0.
        # for com in set(partition.values()):
        #     count = count + 1.
        #     list_nodes = [nodes for nodes in partition.keys()
        #                   if partition[nodes] == com]
        #     nx.draw_networkx_nodes(self.G, pos, list_nodes, node_size=1,
        #                            node_color=str(count / size))
        #
        # nx.draw_networkx_edges(self.G, pos, alpha=0.5)
        #
        # plt.show()
    def degree_centrality_custom(self,G):
        centrality = {}
        s = 1.0
        print (G.degree())
        centrality = dict((n, d * s) for n, d in G.degree_iter())
        return centrality
    def centrality_parser(self):

        self.centrality = {}
        community = ''

        with open(self.folder_name+'/centrality.csv','r') as csvfile:
            reader = csv.reader(csvfile)
            for i in reader:
                if 'Community' in i[0]:
                    self.centrality[i[0]] = {}
                    community = i[0]
                    continue
                self.centrality[community][i[0]]=float(i[1])
    def highest_centrality(self):
        for i in sorted(self.centrality.keys()):

            sorted_cent = sorted(self.centrality[i].items(), key=operator.itemgetter(1), reverse=True)

            count = 0
            high_centrality = []
            for k in sorted_cent:
                high_centrality.append(k)
                count+=1
                if count == 50:
                    break

            with open(self.folder_name+'/highest_centrality.csv', 'a') as csvfile:
                writer = csv.writer(csvfile)
                if len(i) == 11:
                    writer.writerow([int(i[10]),len(self.centrality[i].items())]+high_centrality)
                elif len(i) == 12:
                    writer.writerow([int(i[10:12]),len(self.centrality[i].items())]+high_centrality)
                elif len(i) == 13:
                    writer.writerow([int(i[9:13]),len(self.centrality[i].items())]+high_centrality)
    def writing_classification_result(self):
        for i in self.result:
            with open(self.new_repo_topic_data,'r') as csvfile:
                reader = csv.reader(csvfile)
                with open(self.folder_name+'/'+i+'.csv','a') as csvfile2:
                    writer = csv.writer(csvfile2)
                    for read in reader:
                        for j in self.result[i]:
                            if j in read:
                                writer.writerow([j]+read)