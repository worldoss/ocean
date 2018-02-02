from sna_clustering import *
from pprint import pprint

# 데이터가 저장될 폴더명
folder_name = 'data'
classification_translation = 'Classification/Classification.csv'
new_repo_topic_data = 'new_repo_topic_data.csv'

sna = SNACluster(folder_name,classification_translation,new_repo_topic_data)

# SNA 분석을 위한 그래프 생성
sna.create_graph()
# SNA Clustering 실행
sna.clustering()
# 각 Cluster의 노드별 Centrality 생성
sna.centrality()
# 다음 작업을 위한 Centrality 파싱
sna.centrality_parser()
# 상위 Centrality 별로 Cluster 정렬
sna.highest_centrality()
# 소프트웨어 재분류 결과
sna.writing_classification_result()