# Sorting Tool
=============

### Changelog
- application code dockerised
- SMTP parameters pulled in through environment variables (removes them from the application code)
- app extended with basic logging to file `/app.log`
- optional docker-compose.yml added and Readme updated with detailed instructions for using docker or docker-compose.

## Usage
First, create a '.env' file from the sample provided:
```
cp .env-sample .env
```
and update the parameters as required.

## To run locally, without using docker

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

## To run in docker locally (without docker-compose)
This assumes docker is installed. There is no need to set up a python environment locally.
```
docker build -t sortingtool:latest .
docker run --name sorter --env-file=./.env -d -p 5000:5000 sortingtool
```

## To run in docker on a remote host (without docker-compose or docker-machine)

*Requires docker version >= 18.09*

From the local machine, make sure the image is pushed to a registry that is accessible from the remote host:
```
docker login your-registry.org
docker image tag sortingtool:latest your-registry.org/your-image-naming-convention-sortingtool:latest
docker push your-registry-org/your-image-naming-convention-sortingtool:latest
```
Then set the `DOCKER_HOST` variable to your ssh connection to the remote server 
```
export DOCKER_HOST="ssh://<ssh server>"
```
From now on, docker commands are executed on the remote server (the equivalent of docker -H option).
Note that the --env-file option references a locally stored .env file - there is no need to transfer the .env file to the server.

```bash
# if container already exists from previous run:
docker stop sorter
docker rm sorter
# then
docker run --name sorter --env-file=./.env -d -p 5000:5000 your-registry-org/your-image-naming-convention-sortingtool
```

To unset the DOCKER_HOST variable and return to working with local system:
```
unset DOCKER_HOST
```

## To view logs from the container:
To view logs either view the stdout of the container, or copy the log file with more detailed logs to local disk (level set to INFO in uatapi.py)
```
docker logs sorter
docker cp sorter:/app/app.log .
```
*Note: this will copy over the ssh connection if $DOCKER_HOST is set.*


# Optional: Using docker-compose
## To run in docker, with docker-compose, locally
This assumes docker-compose is installed. On a local machine (mac or pc), docker-compose should already exist - verify with:
```
which docker-compose
docker-compose version
```
To run, verify the contents in `.env`, and then simply execute:
```
docker-compose up -d
```

## To use docker-compose on a remote server
### Option A: run docker-compose on the remote server
#### 1. Install docker-compose on the remote server
Follow step 2 of this guide (requires sudo rights)
https://github.com/NaturalHistoryMuseum/scratchpads2/wiki/Install-Docker-and-Docker-Compose-(Centos-7)

#### 2. transfer the docker-compose.yml file and .env files to the remote server:
This assumes key-based authentication to `<ssh server>`
```
scp .env <ssh server>:/home/<youruser>
scp docker-compose <ssh server>:/home/<youruser>
```
#### 3. ssh to the remote server, and run docker compose
```
[local]$ ssh <ssh server>
[remote]$ docker-compose up -d
```

If you have any sensitive environment variables that you would rather not persist in the .env file, it is possible to edit your docker-compose.yml file as follows to set the value directly from an environment variable set manually on the host:

For example, for the `SMTP_PASS` variable:

Edit .env to remove the password
```
...
SMTP_PASS=dummy
...
```
Edit `docker-compose.yml` to add an `environment` section underneath the env-file specification, which will supercede any variables configured in the .env file with the value of the environment variable on the docker host.
```
     env_file:
      - .env
     environment:
      - SMTP_PASS
```
Then set the `SMTP_PASS` variable in your bash session on the docker host before calling `docker-compose up`:
```
export SMTP_PASS="yourpass"
docker-compose up -d
```
To view your current configuration before starting up, you can always call 
```
docker-compose config
```

## Option B: use local docker-compose to manage remote server
This will work only with docker-compose version >= 1.24 on the local system.

***Note: not yet included on MacOs at time of writing, use Option A above***

Once available, this will be the preferred option, as it avoids having to transfer the docker-compose.yml and .env files to the remote server.

Assuming key-based ssh access to `<ssh sever>`, on the local system:
```
# Re-direct to remote environment.
export DOCKER_HOST="ssh://<ssh sever>"

# Run your docker-compose commands.
docker-compose pull
docker-compose down
docker-compose up

# All docker-compose commands here will be run on remote-host.

# Switch back to your local environment.
unset DOCKER_HOST
```
(from https://stackoverflow.com/a/53524793)
