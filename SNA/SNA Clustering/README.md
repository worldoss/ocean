## SNA Clustering 결과
### 토픽 갯수
* 37,922개

### 전체 저장소 갯수
* 149442개

### 토픽이 없던 저장소
* 114,530개

### 토픽이 있던 저장소
* 34,912개

### Description이 없는 저장소
* 570개

### Topic 전처리 기준
* notword 제외
* 소문자화
* 프로그래밍 언어 제외

### 새로 토픽이 매칭된 저장소
* 138582개
* [topic_with_created_at4.2.csv](https://github.com/worldoss/ocean/blob/master/SNA/SNA%20Clustering/topic_with_created_at4.2.csv)

### 기반/응용 토픽 매칭 결과
* 기반 SW: 27,394개
	* 해외 기반 SW: 27,327개
	* 국내 기반 SW: 57개
	* 토픽별 상위 빈도: 'framework': 5282, 'data': 3889, 'tool': 3502, 'system': 2332, 'development': 1670, 'ui': 1540, 'platform': 1301, 'network': 1233, 'control': 1068, 'os': 1067
* 응용 SW: 11,914개
	* 해외 응용 SW: 11,870개
	* 국내 응용 SW: 44개
	* 토픽별 상위 빈도: 'support': 2414, 'image': 1856, 'language': 1639, 'video': 1024, 'animation': 1005, 'content': 832, '3d': 678, 'streaming': 475, 'rendering': 472, 'virtual': 401, 'recognition': 231

* 추후 개선 사항: support나 framework 와 같은 단어는 기반/응용 동시에 발생하는 경우가 많아서 분류 사전에서 제거해야함, Clustering 을 통해 나온 topic keyword들을 분류사전에 추가할 예정.
(https://github.com/worldoss/ocean/blob/master/SNA/SNA%20Clustering/highest_centrality4.2.csv)

## IITP 산업분류

### 분류 사전
###### 분류 용어의 경우, 서로 중복되는 경우가 많기 때문에 키워드의 정리가 필요, 산업특화 SW의 경우 중복단어를 제거했지만, 시스템, 미들웨어, 응용 SW는가 덜 됨

#### 산업특화 SW(사회기반)

* Construction
* U-City
* Farming
* horticulture
* livestock
* national-defense
* Weapon
* city
* medical
* Hospital
* U-health

#### 산업특화 SW(서비스)

* Game
* Public
* disasters
* disaster
* living
* Criminal
* Medical welfare
* Industrial
* Environmental energy
* Educational
* Logistics
* SCM
* SCP
* SCE
* Shipping
* Container-Carrier
* Bulk-Carrier
* Harbor
* flight
* Airport
* Airline
* Social-media
* E-commerce
* IOT

#### 산업특화 SW(제조)

* Fashion clothes
* Manufacturing
* Avionics
* Flight
* shipbuilding
* e-navigation
* E-Parth
* Car
* Connected
* DTSW
* ship
	
#### 시스템 SW

* Operating 
* Embedded
* os
* Real-Time
* PCServer
* data
* DBMS
* data
* big-data
* system
* integration
* big
* backup
* archiving
* engineering
* test
* development
* virutalization
* hypervisor
* archive
* tool
* serverpc
* resource
* virtualizing
* security
* Certified.
* Access control
* Intrusion detection / defence
* Middleware
* Distributed system SW
* Web application server
* Unified Integration Solution
* TP monitor
* IoT platform
* UI / UX framework
* CDN
* Network security
* Network access control
* Secure communication
* real-time
* distributed
* run
* cloud
* parallel
* it-resource
* incident
* prevention

응용 SW

* image
* recognition
* Video codec / streaming
* Image-writing / editing / synthesis
* CGCCS
* 3D scanning / print
* Modelling / animation / rendering
* Virtual Reality / Augmented Reality
* Holographic / Stereoscopy 3D
* Virtual simulation
* Content distribution
* Content Protection
* Content distribution
* natural language
* informationsequence
* Decision support
* language conversion
* conversational
* Voice recognition
* speech synthesis
* acoustic
* enterprise
* Office wear
* ERP
* SCM
* BI
* CRM
