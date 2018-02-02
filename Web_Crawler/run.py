from Web_Crawler.RepoDetailCollector import *

CSV = '.csv'
REPO_PATH = 'data/'
SAVE_PATH = 'data/results/'

# data 폴더에 저장소 리스트 파일이 있어야함, (test)testlist.csv 참고
repolist_filename = '(test)Repository_data'
repolist_file = REPO_PATH + repolist_filename + CSV

# data/results 폴더에 임시 결과값이 저장됨, (test)temporary_data.csv 참고
save_filename = '(test)temporary_data'
save_file = SAVE_PATH + save_filename + CSV

# data/results 폴더에 결과값이 존재 하지 않거나 에러가 발생한 저장소 이름이 저장됨, (test)error_repository.csv 참고
error_filename = '(test)error_repository'
error_file = SAVE_PATH + error_filename + CSV

# data/results 폴더에 최종 결과값이 저장됨, (test)final_data.csv 참고
final_filename = '(test)final_data'
final_file = SAVE_PATH + final_filename + CSV

repositories = WebCrawler(save_file,error_file,final_file)

with open(repolist_file,'r') as csvfile:
    reader = csv.DictReader(csvfile)
    # 임시 저장 파일 생성
    repositories.CSVCreater()
    for row in reader:
        try:
            # 웹크롤링 시작
            owner,repo = row['full_name'].split('/')
            repositories.data['full_name'] = row['full_name']
            # Github 저장소 HTTP 요청
            repositories.Request(owner,repo)
            # 저장소 별 Commit, Branch, Release, Contributor 값 파싱
            repositories.SummaryScrap()
            # 저장소 별 Topic 값 파싱
            repositories.TopicScrap()
            # 임시 저장 파일에 값 저장
            repositories.CSVWrtier()
        # 존재하지 않거나, 에러가 나는 경우 따로 그 저장소 이름과 결과값이 저장됨
        except ValueError as e:
            print ('ValueError!')
            print (e)
        except IndexError as e:
            print ('IndexError!')
            print (e)
            repositories.ErrorWriter(row['full_name'])
        except NoResultError as e:
            print ('NoResultError!')
            print (e)
            repositories.ErrorWriter(row['full_name'])
            # break
# 임시 저장 파일의 값들을 최정 저장 파일에 저장
repositories.Topic_Parser()
