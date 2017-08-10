#-*- coding: utf-8 -*-

import httplib2
import json
import base64
import csv
import re
from time import sleep

class incompleteError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

class NoresultError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg

lang_popular=[
    'ActionScript',
    'C',
    'CSharp',
    'CPP',
    'Clojure',
    'CoffeeScript',
    'CSS',
    'Go',
    'Haskell',
    'HTML',
    'Java',
    'Javascript',
    'Lua',
    'Matlab',
    'Objective-C',
    'Perl',
    'PHP',
    'Python',
    'R',
    'Ruby',
    'Scala',
    'Shell',
    'Swift',
    'TeX',
    'Vim-script'
]
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
        'Thrift', 'TI-Program', 'TLA', 'TOML', 'Turing', 'Turtle', 'Twig', 'TXL', 'Type-Language', 'TypeScript',
        'Unified-Parallel-C', 'Unity3D-Asset', 'Unix-Assembly', 'Uno', 'UnrealScript', 'UrWeb', 'Vala', 'VCL',
        'Verilog', 'VHDL', 'Visual-Basic', 'Volt', 'Vue', 'Wavefront-Material', 'Wavefront-Object', 'Web-Ontology-Language',
        'WebAssembly', 'WebIDL', 'wisp', 'World-of-Warcraft-Addon-Data', 'X10', 'xBase', 'XC', 'XCompose',
        'XML', 'Xojo', 'XPages', 'XProc', 'XQuery', 'XS', 'XSLT', 'Xtend', 'Yacc', 'YAML', 'YANG', 'Zephir',
        'Zimpl']

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

def Request(url):
    http = httplib2.Http()
    auth = base64.encodestring('rlrlaa123' + ':' + 'ehehdd009')
    return http.request(url,'GET',headers={ 'Authorization' : 'Basic ' + auth})

def WriteCSV(json_parsed,field_name):
    with open('data/1000_star_per_repository_language.csv','a') as csvfile:
        fieldnames = []
        fieldnames_dict = {}
        for field in field_name:
            fieldnames.append(field)
        writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
        for data in json_parsed:
            for field in field_name:
                fieldnames_dict[field]=data[field]
            try:
                writer.writerow(fieldnames_dict)
                fieldnames_dict = {}
            except UnicodeEncodeError as e1:
                with open('data/(test)error_language_1000.csv','a') as csvfile:
                    fieldnames_dict['description']=fieldnames_dict['description'].encode('utf-8')
                    try:
                        writer.writerow(fieldnames_dict)
                        fieldnames_dict = {}
                    except UnicodeEncodeError as e2:
                        errorwriter = csv.writer(csvfile)
                        errorwriter.writerow([fieldnames_dict['full_name'],e2])
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
                WriteCSV(json_parsed,['language','stargazers_count'])
                next = FindLink(response,'next')
                count_last += 1
            else:
                raise incompleteError('Not incomplete results, try again')
        except incompleteError as e:
            print e
        except KeyError as e:
            print e
            sleep(2)
language=lang_popular+lang_others
# Star Count First top 1000 stars respositories per language
for lang in language:
    while True:
        url = 'https://api.github.com/search/repositories?q=stars:>5+language:"'+lang+'"&per_page=100&sort=stars'
        print url
        try:
            response, content = Request(url)
            if json.loads(content)['incomplete_results']==False:
                json_parsed = json.loads(content)['items']
                WriteCSV(json_parsed,['language','stargazers_count'])
                try:
                    next = FindLink(response,'next')
                    last = FindLink(response,'last')
                    NextPage(url,next,last)
                    break
                except KeyError as e:
                    print e
                    break
            else:
                raise incompleteError('Not incomplete results, try again')
        except KeyError as e:
            print e
            sleep(2)


