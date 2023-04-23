# prunner
This is an API for wrapping Linux process created as an assignment for 
Kaspersky SafeBoard. The sample process is a C program that runs for 5 
minutes and prints a statement before exiting
## Cloning repository
```
git clone git@github.com:artemplevako/prunner.git
```
## Building
```
cd prunner
docker build -t prunner .
```
## Running
```
docker run --rm -dp 80:80 prunner
```
You can now try API from your favourite browser by going to 
http://localhost/docs (http://127.0.0.1/docs)
## Cleanup
```
docker image rm prunner
```
