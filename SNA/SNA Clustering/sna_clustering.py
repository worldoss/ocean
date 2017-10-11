# -*- coding: utf-8 -*-

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import csv
import community
import pprint
import operator

class SNA():
    def create_graph(self):
        path = ""
        data = pd.read_csv(path + '../../worldoss:ocean/Web_Crawler/generated_repo_topic_data.csv', error_bad_lines=False, header=None,
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

        print nx.number_of_nodes(self.G)
        print nx.number_of_edges(self.G)

    def centrality(self):

        with open('community_test.csv','rU') as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                cluster = row[1:]
                edges = []
                print cluster
                for i in self.edges:
                    for j in cluster:
                        if i[0] == j:
                            for k in cluster:
                                if i[1] == k:
                                    edges.append(i)
                        if i[1] == j:
                            for k in cluster:
                                if i[0] == k:
                                    edges.append(i)

                C = nx.Graph()
                C.add_nodes_from(cluster)
                C.add_edges_from(edges)

                node_count=nx.number_of_nodes(C)
                edge_count=nx.number_of_edges(C)

                print node_count, edge_count

                cent = self.degree_centrality_custom(C)

                print cent

                with open('centrality_test.csv','a') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerow(['Community '+row[0],'Node: '+str(node_count),'Edge: '+str(edge_count)])
                    for i,j in cent.items():
                        writer.writerow([i,j])
                print 'Finished Community '+row[0]

    def clustering(self):
        partition = community.best_partition(self.G)
        with open('community.csv','a') as csvfile:
            writer = csv.writer(csvfile)
            for community_num in set(partition.values()):
                print "Community", community_num
                members = list_nodes = [nodes for nodes in partition.keys() if partition[nodes] == community_num]
                print members
                writer.writerow([community_num]+members)

    def degree_centrality_custom(self,G):
        centrality = {}
        s = 1.0
        print G.degree()
        centrality = dict((n, d * s) for n, d in G.degree_iter())
        return centrality

    # self.centrality['Community #']
    def centrality_parser(self):

        self.centrality = {}
        community = ''

        with open('centrality2.csv','r') as csvfile:
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
            for k in sorted, _cent:
                high_centrality.append(k)
                count+=1
                if count == 50:
                    break

            with open('highest_centrality2.csv', 'a') as csvfile:
                writer = csv.writer(csvfile)
                if len(i) == 11:
                    writer.writerow([int(i[10]),len(self.centrality[i].items())]+high_centrality)
                elif len(i) == 12:
                    writer.writerow([int(i[10:12]),len(self.centrality[i].items())]+high_centrality)
                elif len(i) == 13:
                    writer.writerow([int(i[9:13]),len(self.centrality[i].items())]+high_centrality)

    def matchrepository(self):
        topic = []
        created = []
        with open('repo_created_at.csv', 'r') as csvfile:
            reader = csv.reader(csvfile)
            for i in reader:
                created.append(i)
        # print created[1]
        with open('new_repo_topic_data2.csv','r') as csvfile:
            reader = csv.reader(csvfile)
            for i,j in enumerate(reader):
                for k in j[1:]:
                    created[i].append(k)
        with open('topic_with_created_at.csv','a') as csvfile:
            writer = csv.writer(csvfile)
            for i in created:
                writer.writerow(i)

sna = SNA()
# sna.create_graph()
# sna.clustering()
# sna.centrality()
sna.centrality_parser()
sna.highest_centrality()
# sna.matchrepository()

# #drawing
# size = float(len(set(partition.values())))
# pos = nx.spring_layout(G)
# count = 0.
# for com in set(partition.values()) :
#     count = count + 1.
#     list_nodes = [nodes for nodes in partition.keys()
#                                 if partition[nodes] == com]
#     nx.draw_networkx_nodes(G, pos, list_nodes, node_size = 1,
#                                 node_color = str(count / size))
#

# nx.draw_networkx_edges(G,pos,alpha=0.5)

# plt.show()
