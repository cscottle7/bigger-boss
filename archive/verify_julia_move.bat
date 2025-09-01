@echo off
echo === VERIFYING DR JULIA FOLDER LOCATION ===
echo.

echo Checking if folder exists locally (should be empty after successful move):
if exist "C:\Users\cscot\Documents\Content\FFL\@drjuliacrawford_com_au" (
    echo WARNING: Local folder still exists
    echo Contents:
    dir "C:\Users\cscot\Documents\Content\FFL\@drjuliacrawford_com_au" /b
) else (
    echo SUCCESS: Local folder has been removed
)
echo.

echo Checking destination on Google Drive:
echo Location: gdrive-shared:Customers/Dr Julia Crawford/SEO/
rclone lsf "gdrive-shared:Customers/Dr Julia Crawford/SEO/" --dirs-only
echo.

echo Checking if @drjuliacrawford_com_au folder exists at destination:
rclone lsf "gdrive-shared:Customers/Dr Julia Crawford/SEO/@drjuliacrawford_com_au/" --max-depth 1
echo.

echo Full path verification:
rclone lsf "gdrive-shared:Customers/Dr Julia Crawford/SEO/@drjuliacrawford_com_au/"
echo.

echo === VERIFICATION COMPLETE ===
pause