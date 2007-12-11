mkdir dist
move db dist
move config dist
Makespec.py --onefile --windowed --debug pubshelf.py
REM Makespec.py --onefile --windowed pubshelf.py
Build.py pubshelf.spec
move pubshelf.exe dist
