# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
import csv
import datetime


file_path = 'file_path'
owner_file_name = 'owner_file_name' + '.csv'
repo_file_name = 'repo_file_name' + '.csv'

repo_data = pd.read_csv(file_path + repo_file_name)
repo_id_list = repo_data.values[:,0]
owner_data_list = repo_data.values[:,3]


def owner_parsing_fn(owner_raw_data):
    owner_raw_data = owner_raw_data.replace('{u', 'u')
    owner_raw_data = owner_raw_data.replace("'}", "'")
    owner_raw_data = owner_raw_data.replace("u'", "'")
    owner_raw_data = owner_raw_data.replace('"', '')
    owner_raw_data = owner_raw_data.replace("'", '')
    owner_raw_data_list = owner_raw_data.split(',')

    owner_data_list = []
    for owner_data in owner_raw_data_list:
        owner_data_list.append(owner_data.split(': '))

    return np.array(owner_data_list)


owner_data_val_name = owner_parsing_fn(owner_data_list[0])[:,0]

with open(file_path + owner_file_name, 'w', newline='') as f:
    f = csv.writer(f)
    f.writerow(['repo_id'] + list(owner_data_val_name) + ['saved_DateTime'])

with open(file_path + owner_file_name, 'a', newline='') as f:
    f = csv.writer(f)
    for owner_raw_data, repo_id in zip(owner_data_list, repo_id_list):
        owner_data_val = owner_parsing_fn(owner_raw_data)[:, 1]
        f.writerow([repo_id] + list(owner_data_val) + [str(datetime.datetime.now())])

print('Complete !')
