@echo OFF
IF "%py26"=="" (
	C:\Python26\python.exe game.py
) ELSE (
	%py26%\python.exe game.py
)
