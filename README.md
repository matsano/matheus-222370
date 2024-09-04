# matheus-222370


docker pull jodogne/orthanc-python

docker run -d --name orthanc -p 4242:4242 -p 8042:8042 jodogne/orthanc-python

docker network create my-network

docker volume create python-scripts-test-volume

docker build -t python-scripts-test .

docker run --network my-network -v python-scripts-test-volume:/app python-scripts-test





https://github.com/jodogne/OrthancDocker
https://medium.com/buildpiper/simplifying-containerization-with-docker-run-command-2f74e114f42a