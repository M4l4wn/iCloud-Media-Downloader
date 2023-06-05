:: "%~dp0DownloadsFileSorter.py" is the relative path to your Python script file. "%~dp0" expands to the drive and path of the .bat file itself, allowing the script to be executed from any directory as long as the .bat file and the script are in the same directory.
@echo off
python "%~dp0iCloudMediaDownloader.py"
pause
