@echo off
echo === CORRECTED DR JULIA FOLDER MOVE ===
echo.

echo Step 1: Checking if source folder exists...
if exist "C:\Users\cscot\Documents\Content\FFL\@drjuliacrawford_com_au" (
    echo FOUND: @drjuliacrawford_com_au folder exists locally
    echo.
    
    echo Step 2: Creating destination directory...
    rclone mkdir "gdrive-shared:Customers/Dr Julia Crawford/SEO/"
    echo.
    
    echo Step 3: Moving folder with CORRECT path...
    rclone move "C:\Users\cscot\Documents\Content\FFL\@drjuliacrawford_com_au" "gdrive-shared:Customers/Dr Julia Crawford/SEO/@drjuliacrawford_com_au"
    echo.
    
    echo Step 4: Verifying the move...
    rclone lsf "gdrive-shared:Customers/Dr Julia Crawford/SEO/" --dirs-only
    echo.
    
    echo Step 5: Listing contents of moved folder...
    rclone lsf "gdrive-shared:Customers/Dr Julia Crawford/SEO/@drjuliacrawford_com_au/"
    echo.
    
    echo Move operation completed!
) else (
    echo ERROR: @drjuliacrawford_com_au folder not found locally
    echo The folder may have been moved or renamed already.
)

echo.
echo === OPERATION COMPLETE ===
pause