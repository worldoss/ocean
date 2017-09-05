# -*- coding: utf-8 -*-

import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import csv

file_path = 'C:\\Users\\LG\\Desktop\\'  # 읽어올 데이터 path 설정

data = pd.read_csv(file_path + 'jongmake.csv')     # pandas 라이브러리를 이용해서 csv 파일 읽어오기
# print(data.head())
# print('*'*150)
# print(data.info())


# node 설정
a_node = data.values[:,0]    # a_node = id
b_node = data.values[:,1]    # b_node = repository_name


# edge 설정
edge_list = []
for i, j in zip(a_node, b_node):
    temp = (i,j)
    edge_list.append(temp)
# print(edge_list)

G = nx.Graph()
user_nodes = list(a_node)
repo_nodes = list(set(b_node))
nodes = user_nodes + repo_nodes
edges = [edge_list[0]]
G.add_nodes_from(nodes)
G.add_edges_from(edges)

nx.draw(G)  # 기본 그리기

plt.show()
