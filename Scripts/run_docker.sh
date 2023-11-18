#!/bin/bash

error_exit()
{
    echo "Error: $1" 1>&2
    exit 1
}

HOST_IP=$(ip addr show | grep 'inet ' | grep -v '127.0.0.1' | awk '{print $2}' | cut -d/ -f1 | head -n 1)
if [ -z "$HOST_IP" ]; then
    error_exit "Failed to fetch host IP address"
else
    echo "Host IP address: $HOST_IP"
fi

export HOST_IP

chown 1000:1000 ../jenkins-data || error_exit "Failed to change ownership of ../jenkins-data"

chmod 666 /var/run/docker.sock || error_exit "Failed to set permissions on /var/run/docker.sock"

cd ../Docker || error_exit "Failed to change directory to ../Docker"
docker-compose up -d || error_exit "Docker-compose failed to start up services"

echo "Sleeping for 15 seconds to allow services to stabilize then restarting the jenkins container"
for i in {15..1}; do
    echo -ne "$i seconds left\033[0K\r"
    sleep 1
done

docker restart docker-jenkins-1 || error_exit "Failed to restart docker-jenkins-1 container"

jenkins_ip=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' docker-jenkins-1)
if [ -z "$jenkins_ip" ]; then
    error_exit "Failed to fetch IP address of docker-jenkins-1 container"
else
    echo "Jenkins container IP address: $jenkins_ip"
fi

echo "Script executed successfully."
