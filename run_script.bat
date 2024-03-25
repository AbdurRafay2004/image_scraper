@setlocal enabledelayedexpansion

:: Get the full path of the current script
rem %~dp0 expands to the drive and path of the batch script
set script_dir=%~dp0

cd /d "%script_dir%"

:: Get script name without extension (optional)
rem You can uncomment the following line if you want the script name without extension
rem set script_name=%~n0

:: Call your Python script
python mainpr.py 

endlocal
