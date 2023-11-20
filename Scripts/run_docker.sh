#!/bin/bash

error_exit() {
	echo "Error: $1" 1>&2
	exit 1
}

get_host_ip() {
	if [[ ${OSTYPE} == "darwin"* ]]; then
		# Mac OSX
		HOST_IP=$(ifconfig | grep 'inet ' || true)
		HOST_IP=$(echo "${HOST_IP}" | grep -v '127.0.0.1' || true)
		HOST_IP=$(echo "${HOST_IP}" | awk '{print $2}' || true)
		HOST_IP=$(echo "${HOST_IP}" | head -n 1 || true)
	else
		# Linux/Windows
		HOST_IP=$(ip addr show | grep 'inet ' || true)
		HOST_IP=$(echo "${HOST_IP}" | grep -v '127.0.0.1' || true)
		HOST_IP=$(echo "${HOST_IP}" | awk '{print $2}' || true)
		HOST_IP=$(echo "${HOST_IP}" | cut -d/ -f1 || true)
		HOST_IP=$(echo "${HOST_IP}" | head -n 1 || true)
	fi

	if [[ -z "${HOST_IP}" ]]; then
		error_exit "Failed to fetch host IP address"
	else
		echo "Host IP address: ${HOST_IP}"
	fi

	export HOST_IP
}

change_ownership() {
	if id -u 1000 >/dev/null 2>&1; then
		USER_EXISTS=true
	else
		USER_EXISTS=false
	fi

	if getent group 1000 >/dev/null 2>&1; then
		GROUP_EXISTS=true
	else
		GROUP_EXISTS=false
	fi

	if [[ "${USER_EXISTS}" = true ]] && [[ "${GROUP_EXISTS}" = true ]]; then
		chown 1000:1000 ../jenkins-data || error_exit "Failed to change ownership of ../jenkins-data"
	else
		echo "User or group with ID 1000 does not exist. Skipping ownership change."
	fi
}

set_permissions() {
	if [[ -e /var/run/docker.sock ]]; then
		chmod 666 /var/run/docker.sock || error_exit "Failed to set permissions on /var/run/docker.sock"
	else
		echo "/var/run/docker.sock does not exist. Skipping permission change."
	fi
}

start_docker() {
	if [[ -d ../Docker ]]; then
		cd ../Docker || error_exit "Failed to change directory to ../Docker"
		HOSTNAME=$(hostname)
		if [ "$HOSTNAME" == "LAPTOP-LTRUU0OS" ]; then
 			docker compose up -d || error_exit "docker compose failed to start up services"
		else
			docker-compose up -d || error_exit "Docker-compose failed to start up services"
		fi
	else
		echo "../Docker directory does not exist. Skipping Docker start."
	
	fi
}

restart_jenkins() {
	echo "Sleeping for 15 seconds to allow services to stabilize then restarting the jenkins container"
	for i in {15..1}; do
		echo -ne "${i} seconds left\033[0K\r"
		sleep 1
	done

	docker restart docker-jenkins-1 || error_exit "Failed to restart docker-jenkins-1 container"
}

main() {
	get_host_ip
	change_ownership
	set_permissions
	start_docker
	restart_jenkins
}

main
