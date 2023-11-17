#!/bin/bash

chown 1000:1000 ../jenkins-data

chmod 666 /var/run/docker.sock

cd ../Docker && docker-compose up -d
