from SNA.bigquery_event_collector import *
import datetime

if __name__ == "__main__":
    # 시작시간
    print(datetime.datetime.now())
    # 저장 폴더명
    folder_name = 'System_20180116'
    # 저장소 리스트 파일 - 헤더가 없어야함!
    get_repository_from = '(test)system_original.csv'
    # Github API를 위한 깃허브 계정
    id = 'rlrlaa123'
    pw = 'ehehdd009'

    bquery = EventAnalysis(folder_name)
    # 저장소 리스트 생성
    bquery.getRepositories(get_repository_from)
    for repo in bquery.REPOSITORY:
        # Bigquery API 이벤트 수집
        bquery.collectEvent(repo,id, pw)
        # 각 이벤트 별 SNA 분석
        bquery.snaAnalysis(repo)
        # 이벤트 빈도별 유저 타입 카운팅
        bquery.typeCount(repo)
        # 이벤트 빈도별 유저 타입 분류
        bquery.userCategorize(repo)
    # 저장소 별 유저 타입 빈도
    bquery.categorizedUserCount()
    # 저장소 별 SNA 밀도값
    bquery.snaDensity()
    # 저장소 별 유저 타입 비율
    bquery.countRatio()
    # 저장소 별 SNA 지표 최대/평균값
    bquery.snaMaxAvg()
    # 종료시간
    print(datetime.datetime.now())