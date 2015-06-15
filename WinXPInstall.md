#WinXP 에서 설치하는 방법

# 기본적으로 설치해야 하는 것들 #
  * tortoisesvn ( http://tortoisesvn.net/downloads ) -- ver. 1.4.4
  * sqlite3 ( http://www.sqlite.org/download.html ) -- ver. 3.4.0
  * python ( http://www.python.org/download/ ) -- ver. 2.5.1 (**2.5 이상**)
  * wxpython ( http://www.wxpython.org/download.php ) -- ver. 2.8.4 unicode 버전
  * PyYAML ( http://pyyaml.org/wiki/PyYAML ) -- ver.3.0.5

# 소스 받아오기 using TortoiseSVN (탐색기에서 마우스 오른쪽 버튼으로 Checkout) #
  * URL of repository - http://pubshelf.googlecode.com/svn/trunk/
  * Checkout directory - C:\pubshelf

# 설치 #
  * C:\pubshelf\config\pubshelf.tmpl 파일을 C:\pubshelf\config\pubshelf.yaml 로 복사하고 내용 수정
  * sqlite3.exe 실행 파일을 c:\pubshelf 로 옮김
  * cmd 창 띄워서 다음 명령 실행
  * cd C:\
  * cd pubshelf\
  * sqlite3 db\pubshelf.db < config\schema.sqlite3.sql
  * C:\Python25\python pubshelf.py