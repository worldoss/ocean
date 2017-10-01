import csv
import time


####################################################################################################

repo_owner_file_path = 'repo_owner_file_path/'
repo_owner_file_name = 'repo_owner_file_name.csv'

korea_user_file_path = 'korea_user_file_path/'
korea_user_file_name = 'korea_user_file_name.csv'

korea_repo_file_path = 'korea_repo_file_path/'
korea_repo_file_name = 'korea_repo_file_name.csv'

####################################################################################################


start = time.time()
point_line = '*'*150
double_point_line = point_line + '\n' + point_line

repo_id_list = []
owner_id_list = []
with open(repo_owner_file_path + repo_owner_file_name, 'r') as f_open:
    reader = csv.DictReader(f_open)
    for row in reader:
        repo_id_list.append(row['repo_id'])
        owner_id_list.append(row[' id'])

korea_user_login_list = []
korea_user_id_list = []
korea_user_type_list = []
korea_user_search_location_list = []
with open(korea_user_file_path + korea_user_file_name, 'r') as f_open:
    reader = csv.DictReader(f_open)
    for row in reader:
        korea_user_login_list.append(row['user_name'])
        korea_user_id_list.append(row['user_id'])
        korea_user_type_list.append(row['type'])
        korea_user_search_location_list.append(row['search_location'])

with open(korea_repo_file_path + korea_repo_file_name, 'w') as f_open:
    f = csv.writer(f_open)
    f.writerow(['repo_id', 'owner_id', 'owner_name', 'type', 'search_location'])

f_open = open(korea_repo_file_path + korea_repo_file_name, 'a')
f = csv.writer(f_open)
per = 0
for i in range(len(korea_user_id_list)):
    for j in range(len(owner_id_list)):
        running_per = float((i * j) * 100) / (len(korea_user_id_list) * len(owner_id_list))
        if running_per >= per:
            print '%0.2f'%running_per, '%'
            per += 0.01
        if korea_user_id_list[i] == owner_id_list[j]:
            # print repo_id_list[j], owner_id_list[j], korea_user_login_list[i], korea_user_type_list[i], korea_user_search_location_list[i]
            f.writerow([repo_id_list[j], owner_id_list[j], korea_user_login_list[i], korea_user_type_list[i], korea_user_search_location_list[i]])

print 'Complete !'
end = time.time()
print '\n\n' + double_point_line + '\n\nRunning_Time : %0.4f'%((end-start)/60) + 'm\n\n' + double_point_line
