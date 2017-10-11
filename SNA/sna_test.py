# -*- coding: utf-8 -*-

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import csv
 

path = "D:\\Paul_ds\\01_IBIS_paul\\PycharmProjects\\Github_SNA\\"
data = pd.read_csv(path + 'jongmake.csv')     # pandas 라이브러리를 이용해서 SNA 분석 csv 파일 불러오기
 
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
    
G = nx.DiGraph()
G.add_nodes_from(nodes)
G.add_edges_from(edge_list)

# 만들어진 네트워크 타입, 노드 수, 엣지 수, in/out 평균 degree 확인
print(nx.info(G))

# edge list Visualization
nx.draw_networkx(G)  
plt.show()
 
# centralities
def central_list(E):
    return nx.degree_centrality(E), nx.closeness_centrality(E), nx.betweenness_centrality(E), nx.eigenvector_centrality(E)

central_list(G)
c1 = nx.degree_centrality(G)
c2 = nx.closeness_centrality(G)
c3 = nx.betweenness_centrality(G)
c4 = nx.eigenvector_centrality(G)

# degree Top-30 확인    
def sorting(E):
    sorting_c1 = sorted(c1.items(), key=lambda x: x[1], reverse=True)[:30]  # 예시데이터 기준 30개의 중심성 순위 정렬
    sorting_c2 = sorted(c2.items(), key=lambda x: x[1], reverse=True)[:30]
    sorting_c3 = sorted(c3.items(), key=lambda x: x[1], reverse=True)[:30]
    sorting_c4 = sorted(c4.items(), key=lambda x: x[1], reverse=True)[:30]

    return sorting_c1, sorting_c2, sorting_C3, sorting_c4

sorting = sorting(G)
print(sorting)

# density
def density(Network):
    density = []    
    density.append(round(nx.density(G)))
   
# adjacent matrix
adj = nx.adj_matrix(G)
adj_G =adj.todense()

# 출력파일 저장(User)
file_path = 'C:\\Users\\LG\Desktop\\'
file_name = 'centralities_user.csv'

header_user = ['user', 'degree_central', 'closeness_central', 'betweenness_central', 'eigenvector_central']

with open(file_path + file_name, 'w', newline='', encoding='utf-8') as f:
    csv_write = csv.writer(f)
    csv_write.writerow(header_user)
  
with open(file_path + file_name, 'a', newline='', encoding='utf-8') as f:
    csv_write = csv.writer(f)
    for name in user_nodes:
        csv_writer.writerow([name]+[c1[name]]+[c2[name]]+[c3[name]]+[c4[name]])

# 출력파일 저장(reposiroty)
file_name = 'centralities_repository.csv'
header_repo = ['repository', 'degree_central', 'closeness_central', 'betweenness_central', 'eigenvector_central']

with open(file_path + file_name, 'w', newline='', encoding='utf-8') as f:
    csv_write = csv.writer(f)
    csv_write.writerow(header_repo)
   
with open(file_path + file_name, 'a', newline='', encoding='utf-8') as f:
    csv_write = csv.writer(f)
    for name in repo_nodes:
        csv_write.writerow([name]+[c1[name]]+[c2[name]]+[c3[name]]+[c4[name]])
