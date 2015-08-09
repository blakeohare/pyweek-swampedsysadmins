@echo OFF
IF "%py27"=="" (
	C:\Python27\python.exe game.py
) ELSE (
	%py27%\python.exe game.py
)
