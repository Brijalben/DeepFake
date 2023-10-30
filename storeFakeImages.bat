@echo off
:loop
:: Generate a unique filename based on date and time
for /f "tokens=1-6 delims=:/-. " %%a in ("%date% %time%") do (
    set filename=%%d%%c%%b_%%e%%f
)
:: Define the Wasabi S3 bucket and folder
set endpoint_url=--endpoint-url=https://s3.ca-central-1.wasabisys.com
set wasabi_bucket=deepfake
set folder_name=Fake
set s3_path=s3:://%wasabi_bucket%/%folder_name%/

:: Download the image
curl -o temp.png https://thispersondoesnotexist.com

:: Check if the download was successful (Exit Code 0)
if %errorlevel% equ 0 (
  echo File Downloaded Successfully uploading file to %s3_path% %endpoint_url%

  :: Upload the image to Wasabi S3
  aws s3 cp temp.png s3://deepfake/Fake/%filename%.png --endpoint-url=https://s3.ca-central-1.wasabisys.com
) else (
   echo "Download failed. Retrying in 60 seconds..."
)

:: Remove the downloaded image
del temp.png

:: Wait for some time before the next download (e.g., 60 seconds)
timeout /t 60 /nobreak

:: Repeat the loop
goto :loop