@echo off
echo === DIAGNOSTIC: LOOKING FOR DR JULIA FOLDER ===
echo.

echo 1. Checking if @drjuliacrawford_com_au still exists locally...
if exist "C:\Users\cscot\Documents\Content\FFL\@drjuliacrawford_com_au" (
    echo FOUND: Local folder @drjuliacrawford_com_au still exists
    dir "C:\Users\cscot\Documents\Content\FFL\@drjuliacrawford_com_au"
) else (
    echo NOT FOUND: Local folder @drjuliacrawford_com_au does not exist
)
echo.

echo 2. Checking destination directory contents...
rclone lsf "gdrive-shared:Customers/Dr Julia Crawford/SEO/" --dirs-only
echo.

echo 3. Checking parent directory...
rclone lsf "gdrive-shared:Customers/Dr Julia Crawford/" --dirs-only
echo.

echo 4. Searching for any julia-related folders on shared drive...
rclone lsf "gdrive-shared:" -R --include "*julia*" --dirs-only
echo.

echo 5. Searching for drjuliacrawford...
rclone lsf "gdrive-shared:" -R --include "*drjuliacrawford*" --dirs-only
echo.

echo === DIAGNOSTIC COMPLETE ===