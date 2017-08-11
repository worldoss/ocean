#-*- coding: utf-8 -*-

# Search 수를 최소화 하기 위해 search 결과 중 가장 낮은 수의 스타 수를 구해야 함
# Other Language의 경우, 너무 많기 때문에 웹에서 리스트를 크롤링 해오고, 그 리스트를
# 사용해서, 결과 중 가장 낮은 수의 스타 수를 구함

# 리스트를 구한 후 띄어쓰기를 없애줘야하고, 각종 에러가 발생하는 언어들을 걸러줘야 하기 때문에
# 결과값은 콘솔에만 print 됨

import httplib2
import json
import base64
import csv
from time import sleep
from bs4 import BeautifulSoup
import urllib
import re

# Github 로그인 ID PW 입력
def Request(url):
    http = httplib2.Http()
    auth = base64.encodestring('id' + ':' + 'pw')
    return http.request(url,'GET',headers={ 'Authorization' : 'Basic ' + auth})

def FindLink(response,which):
    if which == 'next':
        return re.compile('([0-9]+)>; rel="next"').findall(response['link'])
    elif which == 'last':
        return re.compile('([0-9]+)>; rel="last"').findall(response['link'])

# Other Language 리스트를 웹에서 불러옴 (콘솔에 출력)
def OtherLanguageFromWeb():
    fp = urllib.urlopen('https://github.com/search/advanced')
    source = fp.read()
    fp.close()
    soup = BeautifulSoup(source, 'html.parser')
    li = re.compile('<option value="(.+)">').findall(soup.prettify())

    lang_others = []
    for strin in li:
        lang_others.append(str(strin))

    print lang_others

# Other Language 중 search 결과 중 가장 낮은 수의 스타 수 구함 (콘솔에 출력)
# 띄어쓰기가 들어간 언어의 경우 blankList.csv라는 파일에 리스트가 저장됨, 리스트에서 이러한 언어들의 띄어쓰기를 '-'로 대체해 줘야함
def GetOtherLanguage1000thStar():
    lang_others_dict={}
    # 428 languages
    lang_others=[
        '1C-Enterprise', 'ABAP', 'ABNF', 'Ada', 'Agda',
        'AGS-Script', 'Alloy', 'Alpine-Abuild', 'AMPL',
        'Ant-Build-System', 'ANTLR', 'ApacheConf', 'Apex',
        'API-Blueprint', 'APL', 'Apollo-Guidance-Computer',
        'AppleScript', 'Arc', 'Arduino', 'AsciiDoc', 'ASN.1',
        'ASP', 'AspectJ', 'Assembly', 'ATS', 'Augeas', 'AutoHotkey',
        'AutoIt', 'Awk', 'Batchfile', 'Befunge', 'Bison', 'BitBake',
        'Blade', 'BlitzBasic', 'BlitzMax', 'Bluespec', 'Boo',
        'Brainfuck', 'Brightscript', 'Bro', 'C-ObjDump', 'C2hs-Haskell',
        "Cap'n-Proto", 'CartoCSS', 'Ceylon', 'Chapel', 'Charity', 'ChucK',
        'Cirru', 'Clarion', 'Clean', 'Click', 'CLIPS', 'Closure-Templates',
        'CMake', 'COBOL', 'ColdFusion', 'ColdFusion-CFC', 'COLLADA',
        'Common-Lisp', 'Component-Pascal', 'Cool', 'Coq', 'Cpp-ObjDump',
        'Creole', 'Crystal', 'CSON', 'Csound', 'Csound-Document', 'Csound-Score',
        'CSV', 'Cuda', 'CWeb', 'Cycript', 'Cython', 'D', 'D-ObjDump', 'Darcs-Patch',
        'Dart', 'desktop', 'Diff', 'DIGITAL-Command-Language', 'DM', 'DNS-Zone',
        'Dockerfile', 'Dogescript', 'DTrace', 'Dylan', 'E', 'Eagle', 'Easybuild',
        'EBNF', 'eC', 'Ecere-Projects', 'ECL', 'ECLiPSe', 'edn', 'Eiffel', 'EJS',
        'Elixir', 'Elm', 'Emacs-Lisp', 'EmberScript', 'EQ', 'Erlang', 'F#', 'Factor',
        'Fancy', 'Fantom', 'Filebench-WML', 'Filterscript', 'fish', 'FLUX', 'Formatted',
        'Forth', 'Fortran', 'FreeMarker', 'Frege', 'G-code', 'Game-Maker-Language', 'GAS',
        'GAP', 'GCC-Machine-Description', 'GDB', 'GDScript', 'Genie', 'Genshi', 'Gentoo-Ebuild',
        'Gentoo-Eclass', 'Gettext-Catalog', 'Gherkin', 'GLSL', 'Glyph', 'GN', 'Gnuplot', 'Golo',
        'Gosu', 'Grace', 'Gradle', 'Grammatical-Framework', 'Graph-Modeling-Language', 'GraphQL',
        'Graphviz-(DOT)', 'Groovy', 'Groovy-Server-Pages', 'Hack', 'Haml', 'Handlebars', 'Harbour',
        'Haxe', 'HCL', 'HLSL', 'HTML+Django', 'HTML+ECR', 'HTML+EEX', 'HTML+ERB', 'HTML+PHP', 'HTTP',
        'Hy', 'HyPhy', 'IDL', 'Idris', 'IGOR-Pro', 'Inform-7', 'INI', 'Inno-Setup', 'Io', 'Ioke', 'IRC-log',
        'Isabelle', 'Isabelle-ROOT', 'J', 'Jasmin', 'Java-Server-Pages', 'JFlex', 'Jison',
        'Jison-Lex', 'Jolie', 'JSON', 'JSON5', 'JSONiq', 'JSONLD', 'JSX', 'Julia', 'Jupyter-Notebook',
        'KiCad', 'Kit', 'Kotlin', 'KRL', 'LabVIEW', 'Lasso', 'Latte', 'Lean', 'Less', 'Lex',
        'LFE', 'LilyPond', 'Limbo', 'Linker-Script', 'Linux-Kernel-Module', 'Liquid', 'Literate-Agda',
        'Literate-CoffeeScript', 'Literate-Haskell', 'LiveScript', 'LLVM', 'Logos', 'Logtalk', 'LOLCODE',
        'LookML', 'LoomScript', 'LSL', 'M', 'M4', 'M4Sugar', 'Makefile', 'Mako', 'Markdown', 'Marko', 'Mask',
        'Mathematica', 'Maven-POM', 'Max', 'MAXScript', 'MediaWiki', 'Mercury', 'Meson', 'Metal', 'MiniD', 'Mirah',
        'Modelica', 'Modula-2', 'Module-Management-System', 'Monkey', 'Moocode', 'MoonScript', 'MQL4', 'MQL5', 'MTML',
        'MUF', 'mupad', 'Myghty', 'NCL', 'Nemerle', 'nesC', 'NetLinx', 'NetLinx+ERB', 'NetLogo', 'NewLisp', 'Nginx',
        'Nim', 'Ninja', 'Nit', 'Nix', 'NL', 'NSIS', 'Nu', 'NumPy', 'ObjDump', 'Objective-C++', 'Objective-J',
        'OCaml', 'Omgrofl', 'ooc', 'Opa', 'Opal', 'OpenCL', 'OpenEdge-ABL', 'OpenRC-runscript', 'OpenSCAD',
        'OpenType-Feature-File', 'Org', 'Ox', 'Oxygene', 'Oz', 'P4', 'Pan', 'Papyrus', 'Parrot', 'Parrot-Assembly',
        'Parrot-Internal-Representation', 'Pascal', 'PAWN', 'Pep8', 'Perl-6', 'Pic', 'Pickle',
        'PicoLisp', 'PigLatin', 'Pike', 'PLpgSQL', 'PLSQL', 'Pod', 'PogoScript', 'Pony', 'PostScript',
        'POV-Ray-SDL', 'PowerBuilder', 'PowerShell', 'Processing', 'Prolog', 'Propeller-Spin', 'Protocol-Buffer',
        'Public-Key', 'Pug', 'Puppet', 'Pure-Data', 'PureBasic', 'PureScript', 'Python-console', 'Python-traceback',
        'QMake', 'QML', 'Racket', 'Ragel', 'RAML', 'Rascal', 'Raw-token-data', 'RDoc', 'REALbasic', 'Reason', 'Rebol',
        'Red', 'Redcode', 'Regular-Expression', "Ren'Py", 'RenderScript', 'reStructuredText', 'REXX', 'RHTML', 'Ring',
        'RMarkdown', 'RobotFramework', 'Roff', 'Rouge', 'RPM-Spec', 'RUNOFF', 'Rust', 'Sage', 'SaltStack', 'SAS', 'Sass',
        'Scaml', 'Scheme', 'Scilab', 'SCSS', 'Self', 'ShaderLab', 'ShellSession', 'Shen', 'Slash', 'Slim', 'Smali',
        'Smalltalk', 'Smarty', 'SMT', 'SourcePawn', 'SPARQL', 'Spline-Font-Database', 'SQF', 'SQL', 'SQLPL',
        'Squirrel', 'SRecode-Template', 'Stan', 'Standard-ML', 'Stata', 'STON', 'Stylus', 'Sublime-Text-Config',
        'SubRip-Text', 'SuperCollider', 'SVG', 'SystemVerilog', 'Tcl', 'Tcsh', 'Tea', 'Terra', 'Text', 'Textile',
        'Thrift', 'TI-Program', 'TLA', 'TOML', 'Turing', 'Turtle', 'Twig', 'TXL',
        'Type-Language', 'TypeScript',
        'Unified-Parallel-C', 'Unity3D-Asset', 'Unix-Assembly', 'Uno', 'UnrealScript', 'UrWeb', 'Vala', 'VCL',
        'Verilog', 'VHDL', 'Visual-Basic', 'Volt', 'Vue', 'Wavefront-Material', 'Wavefront-Object', 'Web-Ontology-Language',
        'WebAssembly', 'WebIDL', 'wisp', 'World-of-Warcraft-Addon-Data', 'X10', 'xBase', 'XC', 'XCompose',
        'XML', 'Xojo', 'XPages', 'XProc', 'XQuery', 'XS', 'XSLT', 'Xtend', 'Yacc', 'YAML', 'YANG', 'Zephir',
        'Zimpl']
    for lang in lang_others:
        url = 'https://api.github.com/search/repositories?q=stars:>5+language:"'+lang+'"&sort=stars'
        print url
        while(True):
            try:
                response, content = Request(url)
                if json.loads(content)['incomplete_results']==False:
                    if json.loads(content)['total_count'] != 0:
                        if 'link' not in response:
                            print 'one page'
                            star=json.loads(content)['items'][-1]['stargazers_count']
                            print star
                            lang_others_dict[lang]=star
                            print lang_others_dict
                            break
                        else:
                            print 'several pages'
                            last = FindLink(response,'last')
                            last_url = url + '&page='+last[0]
                            print last_url
                            response, content = Request(last_url)
                            star=json.loads(content)['items'][-1]['stargazers_count']
                            print star
                            lang_others_dict[lang]=star
                            print lang_others_dict
                            break
                    else:
                        print 'no results'
                        break
                else:
                    print 'incomplete results try again'
            except KeyError as e:
                print 'limit reached...'
                print e
                sleep(2)
            except ValueError as e:
                print 'blank error\n'+lang
                print e
                with open('blankList.csv','a') as csvfile:
                    blankwriter = csv.writer(csvfile)
                    blankwriter.writerow([lang])
                break
    print lang_others_dict
    return lang_others_dict

GetOtherLanguage1000thStar()

# 결과값 (단, 사용시 에러가 발생하는 언어들을 걸러줘야함.)
result={
    'Mercury': 6, 'Mako': 6, 'TypeScript': 63, 'PureBasic': 6,
    'Objective-C++': 6553, 'DTrace': 6, 'Self': 9, 'Lean': 6,
    'Handlebars': 6, 'RenderScript': 6, 'Graphviz-(DOT)': 7,
    'Fortran': 6, 'Ceylon': 6, 'Rebol': 6, 'RobotFramework': 6,
    'XS': 7, 'Frege': 6, 'GAP': 6, 'AspectJ': 6, 'Jupyter-Notebook': 40,
    'NSIS': 6, 'Brightscript': 6, 'AppleScript': 6, 'Elm': 6,
    'SystemVerilog': 6, 'Smali': 6, 'RAML': 6, 'Nginx': 6, 'MTML': 7,
    'Opa': 6, 'Elixir': 20, 'SAS': 6, 'Gettext-Catalog': 6,
    'MQL4': 6, 'MQL5': 9, 'Agda': 6, 'Thrift': 6, 'Logos': 6,
    'SMT': 6, 'HTML+Django': 6553, 'D': 6, 'PowerBuilder': 6,
    'Kotlin': 9, 'NewLisp': 6, 'Crystal': 6, 'Batchfile': 6,
    'Bison': 13, 'Oz': 6, 'Mirah': 7, 'Ox': 6, 'Objective-J': 6,
    'Game-Maker-Language': 6, 'Gosu': 6, 'FreeMarker': 6,
    'WebAssembly': 14, 'HTML+PHP': 6553, 'Cycript': 7, 'Smarty': 6,
    'HTML+ECR': 6553, 'Arc': 6, 'COBOL': 6, 'IGOR-Pro': 7, 'APL': 6,
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
    'P4': 9, 'Isabelle': 7, 'HTML+EEX': 6553, '1C-Enterprise': 6,
    'Hack': 6, 'Metal': 8, 'Clarion': 6, 'Vue': 8, 'ShaderLab': 6,
    'BlitzBasic': 6, 'Modelica': 6, 'JSONiq': 8, 'Boo': 6,
    'AutoIt': 6, 'EQ': 27, 'Visual-Basic': 6, 'HCL': 6,
    'Prolog': 6, 'SourcePawn': 6, 'CMake': 6, 'AMPL': 6,
    'ColdFusion': 6, 'Harbour': 11, 'Grammatical-Framework': 7,
    'Tcl': 6, 'Logtalk': 6, 'Xojo': 6, 'BlitzMax': 6,
    'PigLatin': 6, 'xBase': 6, 'Lasso': 6, 'GLSL': 6,
    'Eiffel': 6, 'Protocol-Buffer': 6, 'VHDL': 6, 'Arduino': 9,
    'Standard-ML': 6, 'Squirrel': 6, 'HTML+ERB': 6553, 'Rascal': 6,
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
    'ChucK': 6, 'Grace': 15, 'ANTLR': 6, 'GDB': 6, 'F#': 36318, 'LoomScript': 207, 'OCaml': 9, 'Diff': 6,
    'Yacc': 6, 'Fantom': 6, 'Zephir': 6, 'Smalltalk': 6, 'DM': 6, 'Ioke': 6, 'Monkey': 6, 'Gnuplot': 6,
    'Inform-7': 6, 'Apex': 6, 'LiveScript': 6, 'Mathematica': 6, 'QMake': 6, 'Rust': 41, 'ABAP': 6, 'Julia': 6,
    'Slash': 6, 'PicoLisp': 6, 'Erlang': 23, 'Pan': 6, 'LookML': 6, 'Eagle': 6, 'Scheme': 6, 'ooc': 6,
    'PogoScript': 6, 'Nim': 6, 'Max': 6, 'GAS': 6553, 'Dart': 6, 'KiCad': 6, 'Nix': 6, 'Common-Lisp': 8,
    'Propeller-Spin': 6, 'Processing': 6, 'Roff': 6, 'XQuery': 6, 'Nit': 6, 'Chapel': 7, 'Coq': 6, 'Dylan': 7,
    'E': 6, 'Xtend': 6, 'Parrot': 6, 'Csound-Document': 8, 'M': 6, 'Papyrus': 7, 'Web-Ontology-Language': 6,
    'CLIPS': 6, 'NetLinx+ERB': 6553, 'CartoCSS': 6, 'Perl-6': 6, 'Clean': 7, 'Alloy': 6, 'Puppet': 6, 'CWeb': 98,
    "Cap'n-Proto": 6, 'REALbasic': 6, 'PLSQL': 6, 'PAWN': 6, 'UnrealScript': 6, 'Pep8': 16, 'Augeas': 13,
    'SQL': 6, 'PureScript': 6, 'Fancy': 6, 'PowerShell': 11, 'Bro': 6, 'wisp': 6, 'NCL': 15, 'Io': 6, 'Racket': 6,
    'Shen': 8, 'SRecode-Template': 10, 'Dogescript': 7, 'nesC': 6, 'Inno-Setup': 6
}
