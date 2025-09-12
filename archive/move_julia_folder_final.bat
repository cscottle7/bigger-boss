@echo off
echo === MOVING @drjuliacrawford_com_au FOLDER TO GOOGLE DRIVE ===
echo.

echo Step 1: Checking current status...
echo.

echo Checking if @drjuliacrawford_com_au exists locally...
if exist "C:\Users\cscot\Documents\Content\FFL\@drjuliacrawford_com_au" (
    echo FOUND: Local folder @drjuliacrawford_com_au exists
    echo Contents:
    dir "C:\Users\cscot\Documents\Content\FFL\@drjuliacrawford_com_au" /b
    echo.
    
    echo Step 2: Ensuring destination directory exists...
    rclone mkdir "gdrive-shared:Customers/Dr Julia Crawford/SEO/"
    echo.
    
    echo Step 3: Moving folder to Google Drive shared drive...
    echo Source: C:\Users\cscot\Documents\Content\FFL\@drjuliacrawford_com_au
    echo Destination: gdrive-shared:Customers/Dr Julia Crawford/SEO/@drjuliacrawford_com_au
    echo.
    
    rclone move "C:\Users\cscot\Documents\Content\FFL\@drjuliacrawford_com_au" "gdrive-shared:Customers/Dr Julia Crawford/SEO/@drjuliacrawford_com_au" --progress
    
    echo.
    echo Step 4: Verifying the move was successful...
    echo Checking destination folder:
    rclone lsf "gdrive-shared:Customers/Dr Julia Crawford/SEO/" --dirs-only
    echo.
    
    echo Contents of moved folder:
    rclone lsf "gdrive-shared:Customers/Dr Julia Crawford/SEO/@drjuliacrawford_com_au/" --max-depth 1
    echo.
    
    echo Step 5: Verifying local folder was removed...
    if exist "C:\Users\cscot\Documents\Content\FFL\@drjuliacrawford_com_au" (
        echo WARNING: Local folder still exists - move may not have completed successfully
    ) else (
        echo SUCCESS: Local folder has been removed - move completed successfully
    )
    
) else (
    echo Local folder @drjuliacrawford_com_au not found.
    echo Checking if it already exists on Google Drive...
    echo.
    
    echo Checking destination:
    rclone lsf "gdrive-shared:Customers/Dr Julia Crawford/SEO/" --dirs-only
    echo.
    
    echo Searching for the folder on shared drive:
    rclone lsf "gdrive-shared:" -R --include "*drjuliacrawford*" --dirs-only
    echo.
    
    if errorlevel 0 (
        echo The folder may have already been moved.
    )
)

echo.
echo === OPERATION COMPLETE ===
pause