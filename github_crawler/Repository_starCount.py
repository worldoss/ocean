#-*- coding: utf-8 -*-

# 스타 순위별로 저장소들을 정렬하고, 원하는 저장소의 양만큼이 몇 star 이상인지 알아내는 작업

# 먼저, search로 나오는 가장 스타가 높은 저장소들을 구하고, 그 이후의 스타 별 저장소 갯수를 카운트함
# Github 로그인 ID PW 입력해주어야 하고 저장할 CSV 파일명들의 경로를 수정해주어야 한다

# 소요시간: 약 9~10시간

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

# Github 로그인 ID PW 입력
def Request(url):
    http = httplib2.Http()
    id = ''
    pw = ''
    auth = base64.encodestring(id + ':' + pw)
    return http.request(url,'GET',headers={ 'Authorization' : 'Basic ' + auth})

# 언어별 1000번째 저장소 스타수
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
    'HLSL': 6, 'Pure-Data': 6, 'Hy': 6, 'XProc': 6, 'XPages': 7,
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
    'Shen': 8, 'SRecode-Template': 10, 'Dogescript': 7, 'nesC': 6, 'Inno-Setup': 6
}

# search 에러가 발생하는 언어들을 걸러낼 리스트
error_language=[]

def FindLink(response,which):
    if which == 'next':
        return re.compile('([0-9]+)>; rel="next"').findall(response['link'])
    elif which == 'last':
        return re.compile('([0-9]+)>; rel="last"').findall(response['link'])

# 저장할 csv 파일명 수정
def TopStarWriteCSV(lang,json_parsed):
    with open('countStar.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        for data in json_parsed:
            writer.writerow([lang[0]] + [data['stargazers_count']] + [1]+[datetime.datetime.now()])

# 저장할 csv 파일명 수정 (TopStarWriteCSV csv 파일명과 일치!)
def UnderStarWriteCSV(lang,count,json_parsed):
    with open('countStar.csv', 'a') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([lang[0]] + [str(count)] + [json_parsed] + [datetime.datetime.now()])

def NextPage(url,next,last):
    count_last = 2
    while count_last<int(last[0])+1:
        try:
            next_url = url + '&page=' + str(next[0])
            print next_url
            response, content = Request(next_url)
            if json.loads(content)['incomplete_results'] == False:
                json_parsed = json.loads(content)['items']
                TopStarWriteCSV(lang,json_parsed)
                next = FindLink(response,'next')
                count_last += 1
            else:
                raise IncompleteError('Not incomplete results, try again')
        except IncompleteError as e:
            print e
        except KeyError as e:
            print 'Limit reached...'
            sleep(2)

lang_thousand = {}
lang_thousand.update(lang_popular)
lang_thousand.update(lang_others)
lang_items=lang_thousand.items()

# Search 결과로 나오는 가장 높은 순위의 저장소들
for lang in lang_items:
    while True:
        url = 'https://api.github.com/search/repositories?q=stars:>5+language:"'+lang[0]+'"&per_page=100&sort=stars'
        print url
        try:
            response, content = Request(url)
            if json.loads(content)['incomplete_results']==False:
                json_parsed = json.loads(content)['items']
                if json_parsed[0]['language'] == lang[0] or json_parsed[0]['language'] == 'C++' or json_parsed[0]['language'] == 'C#':  # C++과 C#은 search 단어가 다르기 때문에 제외
                    TopStarWriteCSV(lang,json_parsed)
                    try:
                        next = FindLink(response,'next')
                        last = FindLink(response,'last')
                        NextPage(url,next,last)
                        break
                    except KeyError:
                        print 'No next page'
                        break
                else:
                    raise LanguageError('Language miss-match')
            else:
                raise IncompleteError('Incomplete results, try again')
        except IncompleteError as e:
            print e
        except LanguageError as e:
            print e
            with open('error_language.csv', 'a') as csvfile:
                errorwriter = csv.writer(csvfile)
                errorwriter.writerow([lang[0],e])
                error_language.append(lang[0])
            break
        except KeyError:
            print 'Limit reached...'
            sleep(2)

# 에러 발생 언어 제외
for error in error_language:
    lang_items.pop(error)

# 1000번째 저장소 이후의 스타수 별 저장소 수
for lang in lang_items:
    count=lang[1]-1
    while count>5:
        url = 'https://api.github.com/search/repositories?q=stars:'+str(count)+'+language:"'+lang[0]+'"&per_page=100'
        print url
        try:
            response, content = Request(url)
            json_parsed =  json.loads(content)['total_count']
            if json.loads(content)['incomplete_results'] == False:
                if int(json_parsed) != 0:
                    print count, json_parsed
                    UnderStarWriteCSV(lang,count,json_parsed)
                    count-=1
                else:
                    raise NoresultError('No results')
            else:
                raise IncompleteError('Incomplete results, try again')
        except IncompleteError as e:
            print e
        except NoresultError as e:
            count-=1
            print e
        except KeyError:
            print 'Limit reached...'
            sleep(1)