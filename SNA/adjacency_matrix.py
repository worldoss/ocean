# -*- coding: UTF-8 -*-

import networkx as nx
from networkx.algorithms import bipartite
from networkx.linalg import incidence_matrix
import pandas as pd
import numpy as np

if __name__ == '__main__':

    data = pd.read_csv('result_2015_total.csv', header=None)  # pandas 라이브러리를 이용해서 csv 파일 읽어오기

    # node 정의
    a_node = data.values[:, 0]  # a_node = User ID
    b_node = data.values[:, 1]  # b_node = repository_name

    # edge list 정의
    edge_list = []
    for i, j in zip(a_node, b_node):
        temp = (i, j)
        edge_list.append(temp)

    # print edge list
    print("** Edge list 작성이 완료되었습니다.")

    # 네트워크 분석용 데이터 변환
    user_nodes = list(set(a_node))
    repo_nodes = list(set(b_node))
    nodes = user_nodes + repo_nodes
    print(repo_nodes)
    print(user_nodes)

    G = nx.Graph()
    G.add_nodes_from(user_nodes, bipartite=0)
    G.add_nodes_from(repo_nodes, bipartite=1)
    G.add_edges_from(edge_list)

    # biadjacency_matrix 작성
    adjacency_matrix = bipartite.biadjacency_matrix(G,row_order=repo_nodes, column_order=user_nodes)
    # print(adjacency_matrix.todense())

    # co_occurence=incidence_matrix(G,nodelist=nodes, edgelist= edge_list, oriented=False)
    # print(co_occurence.todense())


    # # 데이터 프레임 형태로 변환, 행렬 연산 후 변환 주의
    # df_adjacency = pd.DataFrame(adjacency_matrix.todense(), index=repo_nodes, columns=user_nodes)
    # print(df_adjacency)
