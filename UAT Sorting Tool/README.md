# Sorting Tool
=============

### Changelog
- application code dockerised
- SMTP parameters pulled in through environment variables (removes them from the application code)
- app extended with basic logging to file `/app.log`

## Usage
First, reate a '.env' file from the sample provided:
```
cp .env-sample .env
```
and update the parameters as required.

## To run locally

Optional: run inside a conda environment. You can skip this if you dont use conda and your python environment is 2.7 and has the Flask package.
```
conda env create -n flsk -f requirements.txt
source activate flsk
```
Source the environment variables before starting:
```
set -o allexport
source .env
set +o allexport
```
```
python uatapi.py
```

## To run in docker
This assumes docker is installed. There is no need to set up a python environment locally.
```
docker build -t sortingtool:latest .
docker run --name sorter --env-file=./.env -d -p 5000:5000 sortingtool
```
### To view logs from the container:
To view logs either view the stdout of the container, or copy the log file with more detailed logs to local disk (level set to INFO in uatapi.py)
```
docker logs sorter
docker cp sorter:/app/app.log .
```
