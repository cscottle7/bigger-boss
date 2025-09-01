@echo off
echo === TROUBLESHOOTING DR JULIA FOLDER MOVE ===
echo.

echo 1. Checking destination SEO directory:
rclone lsf "gdrive-shared:Customers/Dr Julia Crawford/SEO/" --dirs-only
echo.

echo 2. Checking parent directory:
rclone lsf "gdrive-shared:Customers/Dr Julia Crawford/" --dirs-only
echo.

echo 3. Searching for drjuliacrawford across shared drive:
rclone lsf "gdrive-shared:" -R --include "*drjuliacrawford*" --dirs-only
echo.

echo 4. Broader search for julia:
rclone lsf "gdrive-shared:" -R --include "*julia*" --dirs-only
echo.

echo 5. Checking if files moved individually:
rclone lsf "gdrive-shared:Customers/Dr Julia Crawford/SEO/" --include "*.md"
echo.

echo === TROUBLESHOOTING COMPLETE ===
pause