@echo OFF
IF "%py34"=="" (
	C:\Python34\python.exe game.py
) ELSE (
	%py34%\python.exe game.py
)
