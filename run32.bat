@echo OFF
IF "%py32"=="" (
	C:\Python32\python.exe unpyc.py
	C:\Python32\python.exe game.py
) ELSE (
	%py32%\python.exe unpyc.py
	%py32%\python.exe game.py
)
