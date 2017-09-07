# -*- coding: utf-8 -*-

import pandas as pd
import csv
import time
import datetime


file_path = 'file_path'
owner_file_name = 'owner_file_name' + '.csv'
repo_file_name = 'repo_file_name' + '.csv'

repo_data = pd.read_csv(file_path + repo_file_name)
repo_id_list = repo_data.values[:,0]
owner_data_list = repo_data.values[:,3]

i = 0
for owner_raw_data, repo_id in zip(owner_data_list, repo_id_list):
    owner_raw_data = owner_raw_data.replace('{u','u')
    owner_raw_data = owner_raw_data.replace("'}", "'")
    owner_raw_data = owner_raw_data.replace("u'", "'")
    owner_raw_data = owner_raw_data.replace('"', '')
    owner_raw_data = owner_raw_data.replace("'", '')
    owner_data = owner_raw_data.split(',')

    owner_data_val = []
    if i == 0:
        owner_data_val_name = []
    for j in owner_data:
        j_list = j.split(': ')
        owner_data_val.append(j_list[1])
        if i == 0:
            owner_data_val_name.append(j_list[0])

    if i == 0:
        with open(file_path + owner_file_name, 'w') as f:
            f = csv.writer(f)
            f.writerow(['repo_id'] + owner_data_val_name + ['saved_DateTime'])
        i = 1

    with open(file_path + owner_file_name, 'a') as f:
        f = csv.writer(f)
        f.writerow([repo_id] + owner_data_val + [str(datetime.datetime.now())])

print 'Complete !'
