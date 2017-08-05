# 한국어 위키 데이터 핸들러

## 나무위키 데이터 핸들러

JSON 형식으로 배포되는 나무 위키 데이터베이스를 핸들링합니다. JSON 형식의 데이터는 json으로 로딩합니다. 

    import json

    database_fname = '../data/namuwiki_170327.json'
    with open(database_fname, encoding='utf-8') as f:
        namuwiki = json.load(f)

namuwiki에서 텍스트 부분을 떼어내어 각각을 파일로 만들고 싶다면 다음을 실행하면 됩니다. max_num_files 개의 파일이 들어있는 폴더가 '../data/namuwiki/'에 생성됩니다. redirect되는 대상은 저장되지 않습니다. 

    from namuwiki import to_text, to_graph

    directory = '../data/namuwiki/'
    to_text(namuwiki, directory, max_num_files=10000, debug=False)

'../data/namuwiki/index.txt' 파일과 '../data/namuwiki/redirect.txt' 파일도 함께 생성됩니다. index.txt는 각 폴더/파일에 어떤 entity가 들어있는지 기록된 파일이며, redirect.txt는 redirection 관계가 저장된 파일입니다. to_text()의 결과로 아래와 같은 형식의 파일들이 생성됩니다. 

    -- directory/
     |-- 0/
     |-- 1/
     ...
     |-- index.txt
     |-- redirect.txt

to_graph(namuwiki)를 실행하면 entity에 연결된 나무위키의 다른 entitiies의 링크들이 graph 형식으로 return 됩니다. 파일, 웹사이트는 링크에서 제외됩니다. 

    graph = to_graph(namuwiki)
    graph['I.O.I']

    $ {'YMC엔터테인먼트 소속 아티스트', '걸그룹', '프로듀스 101', '프로젝트 그룹', '한국 아이돌'}

Entity가 저장된 파일을 찾기 위하여 utils.Indexer를 이용할 수 있습니다. Indexer는 index.txt와 redirection.txt를 입력받습니다. 


    from utils import Indexer

    indexer = Indexer('../data/namuwiki/index.txt', '../data/namuwiki/redirect.txt')

Exact match가 없고 redirection만 있는 경우에는 redirect와 similars가 출력됩니다. similars는 입력된 단어가 포함된 다른 모든 entities입니다. 

    indexer('아이오아이')

    $ {'redirect': 'I.O.I',
     'similars': {'아이오아이 유닛_로고.png',
      '아이오아이(I.O.I) 1st 미니앨범 2차 티저이미지 (1).jpg',
      '아이오아이(I.O.I) 1st 미니앨범 2차 티저이미지 (2).jpg',
      '아이오아이(I.O.I) 1st 미니앨범 첫 번째 티저이미지.jpg',
      '아이오아이_로고.png'}}

Exact match가 있으면 해당 폴더/파일 위치와 similars가 출력됩니다. 

    indexer('I.O.I')

    $ {'match': '35/351816',
     'similars': {'I.O.I 갤러리',
      'I.O.I 노래',
      'I.O.I/광고 및 화보',
      'I.O.I/논란',
      'I.O.I/유닛',
      'I.O.I/음반',
      'I.O.I/활동',
      'I.O.I의 괴담시티',
      '결경/I.O.I',
      '김도연(1999)/I.O.I',
      '김소혜(1999)/I.O.I',
      '김청하/I.O.I',
      '나영(프리스틴)/I.O.I',
      '랜선친구 I.O.I',
      '미나(구구단)/I.O.I',
      '세정(구구단)/I.O.I',
      '소미/I.O.I',
      '스탠바이 I.O.I',
      '아이오아이(I.O.I) 1st 미니앨범 2차 티저이미지 (1).jpg',
      '아이오아이(I.O.I) 1st 미니앨범 2차 티저이미지 (2).jpg',
      '아이오아이(I.O.I) 1st 미니앨범 첫 번째 티저이미지.jpg',
      '연정(우주소녀)/I.O.I',
      '정채연/I.O.I',
      '최유정/I.O.I',
      '타임슬립 - I.O.I'}}
