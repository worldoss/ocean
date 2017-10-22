# -*- coding: utf-8 -*-

import httplib2
import urllib2
import json
import base64
import csv
import time


####################################################################################################

idpw_1 = ['id_1','pw_1']
idpw_2 = ['id_2','pw_2']
idpw_3 = ['id_3','pw_3']
idpw_4 = ['id_4','pw_4']
idpw_5 = ['id_5','pw_5']
idpw_6 = ['id_6','pw_6']

idpw_list = [idpw_1, idpw_2, idpw_3, idpw_4, idpw_5, idpw_6]

owner_data_file_path = 'owner_data_file_path/'
owner_data_file_name = 'owner_data_file_name.csv'

owner_full_data_file_path = 'owner_full_data_file_path/'
owner_full_data_file_name = 'owner_full_data_file_name.csv'

owner_search_error_file_path = 'owner_search_error_file_path/'
owner_search_error_file_name = 'owner_search_error_file_name.csv'


####################################################################################################

point_line = '*'*150
double_point_line = point_line + '\n' + point_line

id_pw_num = 0

def Request(url, idpw):
    id = idpw[0]
    pw = idpw[1]
    http = httplib2.Http()
    auth = base64.encodestring(id + ':' + pw)
    return http.request(url, 'GET', headers={'Authorization': 'Basic ' + auth})

def search_owner_field(owner_name, owner_full_data_file_path=owner_full_data_file_path, owner_full_data_file_name=owner_full_data_file_name, idpw_list=idpw_list):
    global id_pw_num
    q_owner_name = urllib2.quote(owner_name)
    url = 'https://api.github.com/users/' + q_owner_name
    f_open = open(owner_full_data_file_path + owner_full_data_file_name, 'w')
    f = csv.writer(f_open)
    while 1:
        respones, content = Request(url=url, idpw=idpw_list[id_pw_num])
        j_data = json.loads(content)

        try:
            if 'API rate limit exceeded for' in j_data['message']:
                print '\t!!!!....limit reached....!!!!'
                id_pw_num = (id_pw_num + 1) % len(idpw_list)
                continue
            elif j_data['message'] == 'Bad credentials':
                print '\t!!!!....Bad credentials....!!!!'
                print '\t!!!!....delete ' + idpw_list[id_pw_num][0] + '....!!!!'
                del idpw_list[id_pw_num]
                id_pw_num = (id_pw_num) % len(idpw_list)
                continue
        except:
            pass
        try:
            if 'Please wait a few minutes before you try again' in j_data['message']:
                print '\t!!!!....WAIT....!!!!'
                for i in range(0, 5):
                    print '.'
                    time.sleep(1)
                continue
        except:
            pass

        f.writerow(['repo_id'] + j_data.keys())

        return j_data.keys()

def search_owner(f_1, f_2, repo_id, owner_name, field_list, idpw_list=idpw_list):
    global id_pw_num
    q_owner_name = urllib2.quote(owner_name)
    url = 'https://api.github.com/users/' + q_owner_name
    while 1:
        print url
        print '\t', idpw_list[id_pw_num][0]
        respones, content = Request(url=url, idpw=idpw_list[id_pw_num])
        j_data = json.loads(content)

        try:
            if 'API rate limit exceeded for' in j_data['message']:
                print '\t!!!!....limit reached....!!!!'
                id_pw_num = (id_pw_num + 1) % len(idpw_list)
                continue
        except:
            pass
        try:
            if j_data['message'] == 'Bad credentials':
                print '\t!!!!....Bad credentials....!!!!'
                print '\t!!!!....delete ' + idpw_list[id_pw_num][0] + '....!!!!'
                del idpw_list[id_pw_num]
                id_pw_num = (id_pw_num) % len(idpw_list)
                continue
        except:
            pass
        try:
            if 'Please wait a few minutes before you try again' in j_data['message']:
                print '\t!!!!....WAIT....!!!!'
                for i in range(0, 5):
                    print '.'
                    time.sleep(1)
                continue
        except:
            pass
        try:
            if j_data['message'] == 'Not Found':
                print '\t!!!!....Not Found....!!!!'
                f_2.writerow([repo_id, owner_name, j_data['message']])
                break
        except:
            pass

        try:
            data_list = []
            for field in field_list:
                try:
                    data_list.append(str(j_data[field]))
                except:
                    en_j_data = j_data[field].encode('utf-8')
                    data_list.append(str(en_j_data))

            f_1.writerow([repo_id] + data_list)
            break
        except:
            try:
                f_2.writerow([repo_id, owner_name, j_data['message']])
            except:
                f_2.writerow([repo_id, owner_name, j_data])
            break
    return f_1_open, f_2_open

start_time = time.time()

repo_id_list = []
owner_name_list = []
with open(owner_data_file_path + owner_data_file_name, 'r') as f_open:
    reader = csv.DictReader(f_open)
    for row in reader:
        repo_id_list.append(row['repo_id'])
        owner_name_list.append(row[' login'])


field_list = search_owner_field(owner_name_list[0])

with open(owner_search_error_file_path + owner_search_error_file_name, 'w') as f_open:
    f = csv.writer(f_open)
    f.writerow(['repo_id', 'user_login', 'error_message'])

with open(owner_full_data_file_path + owner_full_data_file_name, 'a') as f_1_open:
    f_1 = csv.writer(f_1_open)
    with open(owner_search_error_file_path + owner_search_error_file_name, 'a') as f_2_open:
        f_2 = csv.writer(f_2_open)

        i = 0
        for repo_id, owner_name in zip(repo_id_list, owner_name_list):
            print point_line
            i += 1
            running_per = float(i * 100) / len(repo_id_list)
            print '%0.2f'%running_per, '% ('+str(i)+'/'+str(len(repo_id_list))+')'

            search_owner(f_1=f_1, f_2=f_2, repo_id=repo_id, owner_name=owner_name, field_list=field_list)

print double_point_line

end_time = time.time()
print '\n\n' + double_point_line + '\n\nRunning_Time : %0.4f'%((end_time-start_time)/3600) + 'h\n\n' + double_point_line
