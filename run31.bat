@echo OFF
IF "%py31"=="" (
	C:\Python31\python.exe unpyc.py
	C:\Python31\python.exe game.py
) ELSE (
	%py31%\python.exe unpyc.py
	%py31%\python.exe game.py
)
