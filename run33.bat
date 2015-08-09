@echo OFF
IF "%py33"=="" (
	C:\Python33\python.exe game.py
) ELSE (
	%py33%\python.exe game.py
)
