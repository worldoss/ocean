# -*- coding: utf-8 -*-

import httplib2
import urllib2
import json
import base64
import csv
import time


####################################################################################################
# 모든 id_list를 채워둘 필요는 없습니다.
idpw_1 = ['id_1','pw_1']
idpw_2 = ['id_2','pw_2']
idpw_3 = ['id_3','pw_3']
idpw_4 = ['id_4','pw_4']
idpw_5 = ['id_5','pw_5']
idpw_6 = ['id_6','pw_6']

idpw_list = [idpw_1, idpw_2, idpw_3, idpw_4, idpw_5, idpw_6]

file_path = 'file_path'
korea_user_file_name = 'korea_user_file_name'
location_count_file_name = 'location_count_file_name'

search_location_list = ['korea', 'south korea', 'republic of korea', 'seoul', 'incheon', 'busan', 'pusan', 'daegu', 'gwangju', 'daejeon', 'ulsan', 'pangyo', 'pankyo', 'jeju', 'jejudo']
search_location_list.extend(['한국', '대한민국', '서울', '인천', '부산', '대구', '광주', '대전', '울산', '판교', '제주', '제주도'])
remove_location_list = ['north korea', 'pyongyang']

####################################################################################################

date = time.strftime('%x', time.localtime(time.time())).replace('/', '')
korea_user_file_name = korea_user_file_name + date + '.csv'
location_count_file_name = location_count_file_name + date + '.csv'

start_date = '2007-10-01'
end_date = '20' + date[4:] + '-' + date[:2] + '-' + date[2:4]

point_line = '*'*150
double_point_line = point_line + '\n' + point_line

location_count_dict = {}
del_list = []
id_pw_num = 0


def Request(url, idpw):
    id = idpw[0]
    pw = idpw[1]
    http = httplib2.Http()
    auth = base64.encodestring(id + ':' + pw)
    return http.request(url, 'GET', headers={'Authorization': 'Basic ' + auth})

def total_search_location(location_name, file_path=file_path, location_user_data_file_name=korea_user_file_name,
                    del_list=del_list, location_count_dict=location_count_dict, mode=1, idpw_list=idpw_list):
    global id_pw_num
    print '\n\n' + double_point_line
    print '\t' + location_name
    f_open = open(file_path + location_user_data_file_name, 'a')
    f = csv.writer(f_open)
    page = 1
    while page <= 10:
        q_location_name = urllib2.quote('"' + location_name + '"')
        url = 'https://api.github.com/search/users?q=location:' + q_location_name + '&per_page=100&page=' + str(page)
        print point_line
        while 1:
            print location_name + ' / page = ' + str(page) + ' / ' + idpw_list[id_pw_num][0]
            print url
            respones, content = Request(url=url, idpw=idpw_list[id_pw_num])
            j_data = json.loads(content)
            # print j_data
            try:
                if j_data['incomplete_results'] != 0:
                    print '\t!!!!....incomplete_results....!!!!'
                    continue
                elif j_data['items'] == []:
                    print '\t!!!!....empty items....!!!!'
                    f_open.close()
                    return None
            except:
                pass
            try:
                if 'API rate limit exceeded for' in j_data['message']:
                    print '\t!!!!....limit reached....!!!!'
                    id_pw_num = (id_pw_num+1)%len(idpw_list)
                    time.sleep(1)
                    continue
                elif j_data['message'] == 'Bad credentials':
                    print '\t!!!!....Bad credentials....!!!!'
                    print '\t!!!!....delete ' + idpw_list[id_pw_num][0] + '....!!!!'
                    del idpw_list[id_pw_num]
                    id_pw_num = (id_pw_num)%len(idpw_list)
                    continue
            except:
                pass
            if mode:
                location_count_dict[location_name] = j_data['total_count']
            print '\t\t' + location_name + '_count : ', j_data['total_count']
            if j_data['total_count'] <= 1000:
                for j in range(len(j_data['items'])):
                    if j_data['items'][j]['id'] not in del_list:
                        print j_data['items'][j]['login'], j_data['items'][j]['id'], j_data['items'][j]['type'], location_name
                        del_list.append(j_data['items'][j]['id'])
                        if mode:
                            f.writerow([j_data['items'][j]['login'], j_data['items'][j]['id'], j_data['items'][j]['type'], location_name])
                if len(j_data['items']) != 100:
                    f_open.close()
                    return None
                else:
                    page += 1
            else:
                f_open.close()
                return 'day_fn_start'
            break
    f_open.close()
    return None


def day_search_location(location_name, file_path=file_path, location_user_data_file_name=korea_user_file_name,
                    del_list=del_list, start_date=start_date, end_date=end_date, mode=1, idpw_list=idpw_list):
    global id_pw_num
    print '\n\n' + double_point_line
    print '\t' + location_name
    swtich_value = 0
    f_open = open(file_path + location_user_data_file_name, 'a')
    f = csv.writer(f_open)
    for year in range(2007, 2017+1):
        str_year = str(year)
        for month in range(1, 12+1):
            str_month = str(month)
            if len(str_month) == 1:
                str_month = '0' + str_month
            for day in range(1, 31+1):
                str_day = str(day)
                if len(str_day) == 1:
                    str_day = '0' + str_day
                str_date = str_year + '-' + str_month + '-' + str_day
                if str_date == start_date:
                    swtich_value = 1
                if str_date == end_date:
                    f_open.close()
                    return None

                if swtich_value == 1:
                    page = 1
                    while page <= 10:
                        q_location_name = urllib2.quote('"' + location_name + '"')
                        q_str_date = urllib2.quote(str_date)
                        url = 'https://api.github.com/search/users?q=location:' + q_location_name + '+created:' \
                              + q_str_date + '&per_page=100&page=' + str(page)
                        print point_line
                        while 1:
                            print location_name + ' / ' + str_date + ' / page = ' + str(page) + ' / ' + idpw_list[id_pw_num][0]
                            print url
                            respones, content = Request(url=url, idpw=idpw_list[id_pw_num])
                            j_data = json.loads(content)
                            # print j_data
                            try:
                                if j_data['incomplete_results'] != 0:
                                    print '\t!!!!....incomplete_results....!!!!'
                                    continue
                                elif j_data['items'] == []:
                                    page = 11
                                    print '\t!!!!....empty items....!!!!'
                                    break
                            except:
                                pass
                            try:
                                if j_data['message'] == "Validation Failed":
                                    page = 11
                                    print '\t!!!!....Validation Failed....!!!!'
                                    break
                            except:
                                pass
                            try:
                                if 'API rate limit exceeded for' in j_data['message']:
                                    print '\t!!!!....limit reached....!!!!'
                                    id_pw_num = (id_pw_num + 1) % len(idpw_list)
                                    time.sleep(1)
                                    continue
                                elif j_data['message'] == 'Bad credentials':
                                    print '\t!!!!....Bad credentials....!!!!'
                                    print '\t!!!!....delete ' + idpw_list[id_pw_num][0] + '....!!!!'
                                    del idpw_list[id_pw_num]
                                    id_pw_num = (id_pw_num) % len(idpw_list)
                                    continue
                            except:
                                pass
                            try :
                                for j in range(len(j_data['items'])):
                                    if j_data['items'][j]['id'] not in del_list:
                                        print j_data['items'][j]['login'], j_data['items'][j]['id'], j_data['items'][j]['type'], location_name
                                        del_list.append(j_data['items'][j]['id'])
                                        if mode:
                                            f.writerow([j_data['items'][j]['login'], j_data['items'][j]['id'], j_data['items'][j]['type'], location_name])
                                if len(j_data['items']) != 100:
                                    page = 11
                                else:
                                    page += 1
                                break
                            except:
                                print j_data
                                continue
    f_open.close()



start = time.time()
with open(file_path + korea_user_file_name, 'w') as f_open:
    f = csv.writer(f_open)
    f.writerow(['user_name', 'user_id', 'type', 'search_location'])

with open(file_path + location_count_file_name, 'w') as f_open:
    f = csv.writer(f_open)
    f.writerow(['location_name', 'total_count'])

for l_name in remove_location_list:
    day_val = total_search_location(location_name=l_name, file_path=file_path,
                                    location_user_data_file_name=korea_user_file_name,
                                    del_list=del_list, location_count_dict=location_count_dict, mode=0)
    if day_val == 'day_fn_start':
        day_search_location(location_name=l_name, file_path=file_path,
                            location_user_data_file_name=korea_user_file_name,
                            del_list=del_list, start_date=start_date, end_date=end_date, mode=0)

for l_name in search_location_list:
    day_val = total_search_location(location_name=l_name, file_path=file_path,
                                    location_user_data_file_name=korea_user_file_name,
                                    del_list=del_list, location_count_dict=location_count_dict, mode=1)
    if day_val == 'day_fn_start':
        day_search_location(location_name=l_name, file_path=file_path,
                            location_user_data_file_name=korea_user_file_name,
                            del_list=del_list, start_date=start_date, end_date=end_date, mode=1)

print double_point_line + '\n'

with open(file_path + location_count_file_name, 'a') as f_open:
    f = csv.writer(f_open)
    for l_name in search_location_list:
        print l_name +'_total_count : ', location_count_dict[l_name]
        f.writerow([l_name, location_count_dict[l_name]])

end = time.time()

print '\n\n' + double_point_line + '\n\nRunning_Time : %0.4f'%((end-start)/3600) + 'h\n\n' + double_point_line
