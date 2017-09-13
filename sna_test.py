# -*- coding: utf-8 -*-

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import csv

file_path = 'C:\\Users\\LG\\Desktop\\'  #  로컬저장소 상에 분석용 데이터가 위치한 path 설정

data = pd.read_csv(file_path + 'jongmake.csv')     # pandas 라이브러리를 이용해서 csv 파일 읽어오기



# node 정의
a_node = data.values[:,0]    # a_node = User ID
b_node = data.values[:,1]    # b_node = repository_name


# edge list 정의
edge_list = []
for i, j in zip(a_node, b_node):
    temp = (i,j)
    edge_list.append(temp)

# print edge list
print(edge_list)

# 네트워크 분석용 데이터 변환
user_nodes = list(set(a_node))
repo_nodes = list(set(b_node))
nodes = user_nodes + repo_nodes
edges = edge_list

G = nx.DiGraph()
G.add_nodes_from(nodes)
G.add_edges_from(edges)

# positions for all nodes
pos = nx.shell_layout(G)
nx.draw_networkx_nodes(G,pos,node_size=500, node_color='r')
nx.draw_networkx_edges(G,pos,edgelist=edges, width=0.5)

# labels
nx.draw_networkx_labels(G,pos)

# edge list Visualization
nx.draw_networkx(G)  
plt.show()

# 주요 중심성 지표 계산 함수 추가
def centralissimo(E):
  centralities = []
  centralities.append(nx.in_degree_centrality(E))
  centralities.append(nx.out_degree_centrality(E))
  centralities.append(nx.closeness_centrality(E))
  centralities.append(nx.betweenness_centrality(E))
  centralities.append(nx.eigenvector_centrality(E))
  centralities.append(nx.pagerank(E))

  for node in E.nodes_iter():
    measures = ("\t").join(map(lambda f: str(f[node]), centralities))
    print("%s: %s" % (node, measures))

centralissimo(G)

# 우선순위정렬(중심성)    
in_degree_central = nx.in_degree_centrality(G)
sorted(in_degree_central.items(), key=lambda x: x[1], reverse=True)[:3] # 예시데이터 기준 3개의 repository 중심성 순위 정렬

out_degree_central = nx.out_degree_centrality(G)
sorted(out_degree_central.items(), key=lambda x: x[1], reverse=True)[:10]
