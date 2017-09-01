#-*- coding: utf-8 -*-

# 앞서 github_starCount를 통해 선정된 스타 수를 기준으로 데이터 수집

# 먼저, 먼저, search로 나오는 가장 스타가 높은 저장소들을 모으고, 그 이후의 저장소들을 스타 수 50까지 구함
# Github 로그인 ID PW를 입력하고, 저장소들을 저장할 CSV명을 입력해야함

# 소요시간: 9~10시간

import httplib2
import json
import base64
import csv
import re
import datetime
from time import sleep

class IncompleteError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

class NoresultError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

class LanguageError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

# Popular Language 1000번째 스타 수
lang_popular={
    'ActionScript':10,
    'C':428,
    'CSharp':227,
    'CPP':421,
    'Clojure':64,
    'CoffeeScript':63,
    'CSS':262,
    'Go':475,
    'Haskell':35,
    'HTML':322,
    'Java':1270,
    'JavaScript':2908,
    'Lua':36,
    'Matlab':9,
    'Objective-C':716,
    'Perl':32,
    'PHP':458,
    'Python':1012,
    'R':30,
    'Ruby':600,
    'Scala':75,
    'Shell':215,
    'Swift':359,
    'TeX':15,
    'Vim-script':59
}

# 에러가 발생하는 언어들을 걸러낸 Other Language 리스트
lang_others={
    'Mercury': 6, 'Mako': 6, 'PureBasic': 6,
    'DTrace': 6, 'Self': 9, 'Lean': 6,
    'Handlebars': 6, 'RenderScript': 6, 'Graphviz-(DOT)': 7,
    'Fortran': 6, 'Ceylon': 6, 'Rebol': 6, 'RobotFramework': 6,
    'XS': 7, 'Frege': 6, 'GAP': 6, 'AspectJ': 6, 'Jupyter-Notebook': 40,
    'NSIS': 6, 'Brightscript': 6, 'AppleScript': 6, 'Elm': 6,
    'SystemVerilog': 6, 'Smali': 6, 'RAML': 6, 'Nginx': 6, 'MTML': 7,
    'Opa': 6, 'Elixir': 20, 'SAS': 6, 'Gettext-Catalog': 6,
    'MQL4': 6, 'MQL5': 9, 'Agda': 6, 'Thrift': 6, 'Logos': 6,
    'SMT': 6, 'D': 6, 'PowerBuilder': 6,
    'Kotlin': 9, 'NewLisp': 6, 'Crystal': 6, 'Batchfile': 6,
    'Bison': 13, 'Oz': 6, 'Mirah': 7, 'Ox': 6, 'Objective-J': 6,
    'Game-Maker-Language': 6, 'Gosu': 6, 'FreeMarker': 6,
    'WebAssembly': 14, 'Cycript': 7, 'Smarty': 6,
     'Arc': 6, 'COBOL': 6, 'IGOR-Pro': 7, 'APL': 6,
    'DIGITAL-Command-Language': 6, 'Ring': 145, 'AGS-Script': 7,
    'Cirru': 8, 'SQF': 6, 'Groovy': 13, 'MAXScript': 6, 'Zimpl': 7,
    'OpenSCAD': 6, 'ApacheConf': 6, 'Makefile': 10, 'BitBake': 6,
    'Golo': 8, 'M4': 6, 'LLVM': 6, 'GDScript': 6, 'Verilog': 6,
    'Stata': 6, 'Factor': 6, 'Haxe': 6, 'Forth': 6, 'Red': 6,
    'hlsl': 6, 'Pure-Data': 6, 'Hy': 6, 'XProc': 6, 'XPages': 7,
    'Volt': 6, 'LSL': 6, 'Emacs-Lisp': 32, 'Pascal': 6, 'eC': 7,
    'Terra': 7, 'GCC-Machine-Description': 6, 'Awk': 6, 'UrWeb': 6,
    'Lex': 6, 'Brainfuck': 8, 'Idris': 6, 'REXX': 6, 'LilyPond': 6,
    'PLpgSQL': 6, 'Cool': 6, 'Modula-2': 6, 'AutoHotkey': 6,
    'P4': 9, 'Isabelle': 7, '1C-Enterprise': 6,
    'Hack': 6, 'Metal': 8, 'Clarion': 6, 'Vue': 8, 'ShaderLab': 6,
    'BlitzBasic': 6, 'Modelica': 6, 'JSONiq': 8, 'Boo': 6,
    'AutoIt': 6, 'EQ': 27, 'Visual-Basic': 6, 'HCL': 6,
    'Prolog': 6, 'SourcePawn': 6, 'CMake': 6, 'AMPL': 6,
    'ColdFusion': 6, 'Harbour': 11, 'Grammatical-Framework': 7,
    'Tcl': 6, 'Logtalk': 6, 'Xojo': 6, 'BlitzMax': 6,
    'PigLatin': 6, 'xBase': 6, 'Lasso': 6, 'GLSL': 6,
    'Eiffel': 6, 'Protocol-Buffer': 6, 'VHDL': 6, 'Arduino': 9,
    'Standard-ML': 6, 'Squirrel': 6, 'Rascal': 6,
    'Component-Pascal': 6, 'X10': 7, 'IDL': 6, 'OpenEdge-ABL': 6,
    'ATS': 8, 'Ada': 6, 'SQLPL': 6, 'Jasmin': 9, 'Nu': 6,
    'Limbo': 13, 'POV-Ray-SDL': 6, 'SuperCollider': 6,
    'Oxygene': 6, 'ASP': 6, 'Assembly': 6, 'Kit': 8, 'NetLinx': 10,
    'Turing': 8, 'Vala': 6, 'ECL': 17, 'Bluespec': 7, 'VCL': 7,
    'FLUX': 6, 'NetLogo': 6, 'WebIDL': 34, 'QML': 6, 'Stan': 6,
    'SaltStack': 6, 'Uno': 6, 'Gherkin': 6, 'Charity': 8, 'XML': 6,
    'Pike': 7, 'LOLCODE': 9, 'Liquid': 6, 'XSLT': 6, 'XC': 6,
    'J': 9, 'Mask': 13, 'Genshi': 8, 'EmberScript': 10,
    'MoonScript': 6, 'LabVIEW': 6, 'TLA': 7, 'Nemerle': 6,
    'Cuda': 6, 'KRL': 12, 'Pony': 6, 'Scilab': 6, 'API-Blueprint': 6, "Ren'Py": 6, 'PostScript': 6,
    'ChucK': 6, 'Grace': 15, 'ANTLR': 6, 'GDB': 6, 'LoomScript': 207, 'OCaml': 9, 'Diff': 6,
    'Yacc': 6, 'Fantom': 6, 'Zephir': 6, 'Smalltalk': 6, 'DM': 6, 'Ioke': 6, 'Monkey': 6, 'Gnuplot': 6,
    'Inform-7': 6, 'Apex': 6, 'LiveScript': 6, 'Mathematica': 6, 'QMake': 6, 'Rust': 41, 'ABAP': 6, 'Julia': 6,
    'Slash': 6, 'PicoLisp': 6, 'Erlang': 23, 'Pan': 6, 'LookML': 6, 'Eagle': 6, 'Scheme': 6, 'ooc': 6,
    'PogoScript': 6, 'Nim': 6, 'Max': 6, 'Dart': 6, 'Nix': 6, 'Common-Lisp': 8,
    'Propeller-Spin': 6, 'Processing': 6, 'Roff': 6, 'XQuery': 6, 'Nit': 6, 'Chapel': 7, 'Coq': 6, 'Dylan': 7,
    'E': 6, 'Xtend': 6, 'Parrot': 6, 'Csound-Document': 8, 'M': 6, 'Papyrus': 7, 'Web-Ontology-Language': 6,
    'CLIPS': 6, 'CartoCSS': 6, 'Perl-6': 6, 'Clean': 7, 'Alloy': 6, 'Puppet': 6, 'CWeb': 98,
    "Cap'n-Proto": 6, 'REALbasic': 6, 'PLSQL': 6, 'PAWN': 6, 'UnrealScript': 6, 'Pep8': 16, 'Augeas': 13,
    'SQL': 6, 'PureScript': 6, 'Fancy': 6, 'PowerShell': 11, 'Bro': 6, 'wisp': 6, 'NCL': 15, 'Io': 6, 'Racket': 6,
    'Shen': 8, 'SRecode-Template': 10, 'Dogescript': 7, 'nesC': 6, 'Inno-Setup': 6,
    'HTTP':6,'TypeScript':65,'KiCad':6,'F#': 36318, 'HTML+ERB': 6553, 'HTML+EEX': 6553, 'HTML+PHP': 6553,'HTML+ECR': 6553,'HTML+Django': 6553,'NetLinx+ERB': 6553,'GAS': 6553, 'Objective-C++': 6553
}

# search 에러가 발생할 언어들을 걸러낸 리스트
error_language=[]

field_list=[
    'id','name','full_name',
    'owner','private','html_url',
    'description','fork','url',
    'forks_url','keys_url','keys_url',
    'collaborators_url','teams_url','hooks_url',
    'issue_events_url','events_url','assignees_url',
    'branches_url','tags_url','blobs_url',
    'git_tags_url','git_refs_url','trees_url',
    'statuses_url','languages_url','stargazers_url',
    'contributors_url','subscribers_url','subscription_url',
    'commits_url','git_commits_url','comments_url',
    'issue_comment_url','contents_url','compare_url',
    'merges_url','archive_url','downloads_url',
    'issues_url','pulls_url','milestones_url',
    'notifications_url','labels_url','releases_url',
    'deployments_url','created_at','updated_at',
    'pushed_at','git_url','ssh_url',
    'clone_url','svn_url','homepage',
    'size','stargazers_count','watchers_count',
    'language','has_issues','has_projects',
    'has_downloads','has_wiki','has_pages',
    'forks_count','mirror_url','open_issues_count',
    'forks','open_issues','watchers',
    'default_branch','permissions','score'
]

# Github 로그인 ID PW 입력
def Request(url):
    http = httplib2.Http()
    id = ''
    pw = ''
    auth = base64.encodestring(id + ':' + pw)
    return http.request(url,'GET',headers={ 'Authorization' : 'Basic ' + auth})

# 저장할 csv 파일명 수정
def CreateCSV():
    with open('data/(test)Repository_data.csv', 'a') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=field_list)
        writer.writeheader()

# 저장할 csv 파일명 수정 (CreateCSV csv 파일명과 일치!) + error log 저장할 csv 파일명 따로 수정
def WriteCSV(json_parsed,field_name):
    with open('data/(test)Repository_data.csv','a') as csvfile:
        fieldnames = []
        fieldnames_dict = {}
        for field in field_name:
            fieldnames.append(field)
        fieldnames.append('saved_DateTime')
        for data in json_parsed:
            for field in field_name:
                fieldnames_dict[field]=data[field]
            # Save Time log
            fieldnames_dict['saved_DateTime'] = str(datetime.datetime.now())
            writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
            try:
                writer.writerow(fieldnames_dict)
                fieldnames_dict = {}
            except UnicodeEncodeError as e1:
                    try:
                        fieldnames_dict['description']=fieldnames_dict['description'].encode('utf-8')
                        writer.writerow(fieldnames_dict)
                        fieldnames_dict = {}
                    except UnicodeEncodeError:
                        try:
                            fieldnames_dict['homepage']=fieldnames_dict['homepage'].encode('utf-8')
                            writer.writerow(fieldnames_dict)
                            fieldnames_dict = {}
                        except UnicodeEncodeError as e3:
                            with open('data/error_language.csv', 'a') as csvfile:
                                errorwriter = csv.writer(csvfile)
                                errorwriter.writerow([fieldnames_dict['full_name'],e3])
                                writer.writerow({})
                                fieldnames_dict = {}
                        except AttributeError as e4:
                            with open('data/error_language.csv', 'a') as csvfile:
                                errorwriter = csv.writer(csvfile)
                                errorwriter.writerow([fieldnames_dict['full_name'],e4])
                                writer.writerow({})
                                fieldnames_dict = {}

def FindLink(response,which):
    if which == 'next':
        return re.compile('([0-9]+)>; rel="next"').findall(response['link'])
    elif which == 'last':
        return re.compile('([0-9]+)>; rel="last"').findall(response['link'])

def NextPage(url,next,last):
    count_last = 2
    while count_last<int(last[0])+1:
        try:
            next_url = url + '&page=' + str(next[0])
            print next_url
            response, content = Request(next_url)
            if json.loads(content)['incomplete_results'] == False:
                json_parsed = json.loads(content)['items']
                WriteCSV(json_parsed,field_list)
                next = FindLink(response,'next')
                count_last += 1
            else:
                raise IncompleteError('Incomplete results, try again')
        except IncompleteError as e:
            print e
        except KeyError:
            print 'Limit reached...'
            sleep(2)

lang_thousand = {}
lang_thousand.update(lang_popular)
lang_thousand.update(lang_others)

# CSV파일 초기화
CreateCSV()

# Language 별 스타 수 1000번째 까지의 저장소
lang_key = lang_thousand.keys()
for lang in lang_key:
    while True:
        url = 'https://api.github.com/search/repositories?q=stars:>50+language:"'+str(lang)+'"&per_page=100&sort=stars'
        print url
        try:
            response, content = Request(url)
            if json.loads(content)['incomplete_results']==False:
                print 'Respository count: '+str(json.loads(content)['total_count'])
                if json.loads(content)['total_count'] != 0:
                    json_parsed = json.loads(content)['items']
                    if json_parsed[0]['language'] == lang or json_parsed[0]['language'] == 'C++' or json_parsed[0]['language'] == 'C#': # C++과 C#은 search 단어가 다르기 때문에 제외
                        WriteCSV(json_parsed,field_list)
                        try:
                            next = FindLink(response,'next')
                            last = FindLink(response,'last')
                            # NextPage(url,next,last)
                            break
                        except KeyError as e:
                            print 'No next page'
                            break
                    else:
                        raise LanguageError('Language miss-match')
                else:
                    raise NoresultError('No repository result')
            else:
                raise IncompleteError('Incomplete results, try again')
        except IncompleteError as e:
            print e
        except NoresultError as e:
            print e
            break
        except LanguageError as e:
            print e
            with open('error_language.csv', 'a') as csvfile:
                errorwriter = csv.writer(csvfile)
                errorwriter.writerow([lang,e])
                error_language.append(lang)
            break
        except KeyError as e:
            print 'Limit reached...'
            sleep(2)

# 에러 발생 언어 제외
for error in error_language:
    lang_thousand.pop(error)

# 1000번째 스타 수 이후의 51번째 까지의 저장소
lang_value = lang_thousand.items()
print lang_value
for lang in lang_value:
    print lang
    # 1001번째 star 수 부터 카운트
    count=lang[1]-1
    while count>50:
        url = 'https://api.github.com/search/repositories?q=stars:'+str(count)+'+language:"'+lang[0]+'"&per_page=100&sort=stars'
        print url
        try:
            response, content = Request(url)
            if json.loads(content)['incomplete_results'] == False:
                print 'Repository count: '+str(json.loads(content)['total_count'])
                json_parsed = json.loads(content)['items']
                WriteCSV(json_parsed,field_list)
                try:
                    next = FindLink(response,'next')
                    last = FindLink(response,'last')
                    NextPage(url,next,last)
                    count -= 1
                except KeyError as e:
                    print 'No next page'
                    count -= 1
            else:
                raise IncompleteError('Incomplete results, try again')
        except IncompleteError as e:
            print e
        except KeyError as e:
            print 'Limit reached...'
            sleep(2)