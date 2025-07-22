@echo off
setlocal

:: Define variables
set ZIP_OUTPUT="C:\VideoArchive\ShootingSheetToKodi\plugin.video.random.recursive-master.zip"
set CONTENT_ROOT="c:\Users\Bidon\AppData\Roaming\Kodi\addons\plugin.video.random.recursive\"
set TEMP_DIR="%TEMP%\plugin.video.random.recursive-master"
set EXCLUDE_LIST="*.tmp *.log *.bak release.bat"
set SEVEN_ZIP_PATH="C:\Program Files\7-Zip\7z.exe"

:: Delete the target archive if it exists
if exist %ZIP_OUTPUT% (
    del /q %ZIP_OUTPUT%
    if errorlevel 1 (
        echo Failed to delete existing ZIP archive: %ZIP_OUTPUT%.
        exit /b 1
    )
)

:: Check if 7z.exe is available
if not exist %SEVEN_ZIP_PATH% (
    echo 7-Zip is not installed at the specified path: %SEVEN_ZIP_PATH%. Please install it and try again.
    exit /b 1
)

:: Prepare temporary directory
if exist %TEMP_DIR% rd /s /q %TEMP_DIR%
mkdir %TEMP_DIR%
xcopy /e /i /q %CONTENT_ROOT% %TEMP_DIR% >nul

:: Build exclusion parameters
set EXCLUDE_PARAMS=-xr!.*
for %%E in (%EXCLUDE_LIST%) do (
    set EXCLUDE_PARAMS=!EXCLUDE_PARAMS! -x!%%E
)

:: Pack files into ZIP, including the root folder
echo %SEVEN_ZIP_PATH% a -tzip %ZIP_OUTPUT% %TEMP_DIR% %EXCLUDE_PARAMS%
%SEVEN_ZIP_PATH% a -tzip %ZIP_OUTPUT% %TEMP_DIR% %EXCLUDE_PARAMS%

:: Check if the operation was successful
if errorlevel 1 (
    echo Failed to create ZIP archive.
    exit /b 1
) else (
    echo ZIP archive created successfully: %ZIP_OUTPUT%
)

:: Clean up temporary directory
rd /s /q %TEMP_DIR%

endlocal