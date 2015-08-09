@echo OFF
IF "%py26"=="" (
	C:\Python26\python.exe unpyc.py
	C:\Python26\python.exe game.py
) ELSE (
	%py26%\python.exe unpyc.py
	%py26%\python.exe game.py
)
