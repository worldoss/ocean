import csv
import time
import pandas as pd
from nltk.corpus import stopwords


####################################################################################################

repo_description_and_topic_file_path = ''
repo_description_and_topic_file_name = 'crawling_repo_topic_data.csv'

repo_topic_file_path = ''
repo_topic_file_name = 'new_repo_topic_data2.csv'

remove_topic_list = ['is', 'in', 'of', 'the']
remove_text_list= [',', '.', '/', "'", '"', '(', ')', '{', '}', '[', ']']
stop_words = set(stopwords.words('english'))

####################################################################################################


start = time.time()
point_line = '*'*150
double_point_line = '\n' + point_line + '\n' + point_line + '\n'

repo_description_and_topic_data = pd.read_csv(repo_description_and_topic_file_path + repo_description_and_topic_file_name)
total_data = repo_description_and_topic_data.values

print double_point_line
save_topic_list = []
topic_list = []
per = 0
for i in range(total_data.shape[0]):
    running_per = float(i * 100) / total_data.shape[0]
    if running_per >= per:
        print '%0.1f' % per, '%\t\t', '( ', i, '/', total_data.shape[0], ')'
        per += 0.1
    tmp_save_topic_list = []
    for j in range(2,total_data.shape[1]):
        total_data[i][j] = str(total_data[i][j])
        if total_data[i][j] != 'nan':
            tmp_save_topic_list.append(total_data[i][j])
            if total_data[i][j] not in topic_list:
                topic_list.append(total_data[i][j])
    save_topic_list.append(tmp_save_topic_list)

print topic_list
print len(topic_list)

with open(repo_topic_file_path + repo_topic_file_name, 'w') as f_open:
    f = csv.writer(f_open)
    f.writerow(['repo_full_name', 'topic'])

f_open = open(repo_topic_file_path + repo_topic_file_name, 'a')
f = csv.writer(f_open)

print double_point_line
make_topic_list = []
per = 0
for i in range(total_data.shape[0]):
    running_per = float(i * 100) / total_data.shape[0]
    if running_per >= per:
        print '%0.1f' % per, '%\t\t', '( ', i, '/', total_data.shape[0], ')'
        per += 0.1
    tmp_make_topic_list = []
    description_data = str(total_data[i][1])
    for remove_text in remove_text_list:
        description_data = description_data.replace(remove_text, ' ')
    description_data_list = description_data.split()
    for j in range(len(description_data_list)):
        if description_data_list[j] in topic_list:
            tmp_make_topic_list.append(description_data_list[j])
    make_topic_list.append(tmp_make_topic_list)
    insert_topic_list = list(set(save_topic_list[i] + make_topic_list[i]))

    for remove_topic in stop_words:
        try:
            insert_topic_list.remove(remove_topic)
            # print '\t', 'remove_topic : ', remove_topic
        except:
            pass
    f.writerow([total_data[i][0]] + insert_topic_list)

end = time.time()
print double_point_line + '\nRunning_Time : %0.4f'%((end-start)/60) + 'm\n' + double_point_line
