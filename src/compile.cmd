xcopy C:\Users\%username%\PycharmProjects\Python\Sounder3\*.png C:\Users\%username%\PycharmProjects\Python\Sounder3\dist\Sounder3
xcopy C:\Users\%username%\PycharmProjects\Python\Sounder3\*.ico C:\Users\%username%\PycharmProjects\Python\Sounder3\dist\Sounder3     
xcopy C:\Users\%username%\PycharmProjects\Python\Sounder3\*.txt C:\Users\%username%\PycharmProjects\Python\Sounder3\dist\Sounder3
xcopy C:\Users\%username%\PycharmProjects\Python\Sounder3\*.log C:\Users\%username%\PycharmProjects\Python\Sounder3\dist\Sounder3
xcopy C:\Users\%username%\PycharmProjects\Python\Sounder3\*.json C:\Users\%username%\PycharmProjects\Python\Sounder3\dist\Sounder3
xcopy C:\Users\%username%\PycharmProjects\Python\Sounder3\*.exe C:\Users\%username%\PycharmProjects\Python\Sounder3\dist\Sounder3
ping localhost -n 2 >nul
cd "C:\Users\%username%\Desktop\"
md "Sounder3"
cd "C:\Users\%username%\PycharmProjects\Python\Sounder3\dist\"
xcopy "Sounder3" "C:\Users\%username%\Desktop\Sounder3" /s/h/e/k/f/c
ping localhost -n 2 >nul
cd "C:\Users\%username%\PycharmProjects\Python\Sounder3\"
rd "__pycache__" /s /q
rd "build" /s /q
rd "dist" /s /q
del "Sounder3.spec" /s /q
cls
