@echo off
echo Checking/creating destination path...
rclone mkdir "gdrive-shared:Customers/Dr Julia Crawford/SEO/"

echo Moving folder from local to Google Drive...
rclone move "C:\Users\cscot\Documents\Content\FFL\drjuliacrawford_com_au" "gdrive-shared:Customers/Dr Julia Crawford/SEO/"

echo Listing destination to verify...
rclone ls "gdrive-shared:Customers/Dr Julia Crawford/SEO/"

echo Operation completed!
pause