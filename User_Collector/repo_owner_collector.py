# -*- coding: utf-8 -*-

import numpy as np
import csv


file_path = 'file_path\\'
owner_file_name = 'owner_file_name' + '.csv'
repo_file_name = 'repo_file_name' + '.csv'


def owner_parsing_fn(owner_raw_data_list):
    owner_data_list = []
    replace_text_list = ['{u', "'}", "u'", '"', "'"]
    for owner_data_0 in owner_raw_data_list:
        owner_parsing_data_list = []
        owner_field_name_list = []
        for replace_text in replace_text_list:
            owner_data_0 = owner_data_0.replace(replace_text, '')
        owner_data_1 = owner_data_0.split(',')
        for owner_data_2 in owner_data_1:
            owner_data = owner_data_2.split(': ')
            owner_parsing_data_list.append(owner_data[1])
            owner_field_name_list.append(owner_data[0])
        owner_data_list.append(owner_parsing_data_list)

    return np.array(owner_data_list), np.array(owner_field_name_list)


repo_id_list = []
owner_data_list = []
repo_Saved_DateTime_list = []

with open(file_path + repo_file_name, 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)

    for row in reader:
        repo_id_list.append(row['id'])
        owner_data_list.append(row['owner'])
        repo_Saved_DateTime_list.append(row['Saved_DateTime'])


if repo_id_list == [] or owner_data_list == [] or repo_Saved_DateTime_list == []:
    print 'ERROR !!!!'
    raise FileNotFoundError

owner_final_data, owner_field_data = owner_parsing_fn(owner_data_list)

with open(file_path + owner_file_name, 'w', newline='') as f:
        f = csv.writer(f)
        f.writerow(['repo_id'] + list(owner_field_data) + ['saved_DateTime'])

for owner_raw_data, repo_id, repo_Saved_DateTime in zip(owner_final_data, repo_id_list, repo_Saved_DateTime_list):
    print owner_raw_data

    with open(file_path + owner_file_name, 'a', newline='') as f:
        f = csv.writer(f)
        f.writerow([repo_id] + list(owner_raw_data) + [repo_Saved_DateTime])

print 'Complete !'
