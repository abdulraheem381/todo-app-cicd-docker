#!/bin/bash

# Redirect all output to a log file for debugging
exec > >(tee /var/log/user-data.log|logger -t user-data -s 2>/dev/console) 2>&1

echo "Starting user_data script execution..."

# Wait for cloud-init to finish any apt updates to avoid lock issues
while fuser /var/lib/dpkg/lock >/dev/null 2>&1 ; do echo "Waiting for dpkg lock..."; sleep 1 ; done
while fuser /var/lib/apt/lists/lock >/dev/null 2>&1 ; do echo "Waiting for apt lock..."; sleep 1 ; done

echo "Updating system..."
sudo apt-get update -y

echo "Installing Docker..."
sudo apt-get install -y docker.io docker-compose-plugin

echo "Starting Docker service..."
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker ubuntu

# Create app directory
echo "Setting up app directory..."
sudo mkdir -p /home/ubuntu/app
cd /home/ubuntu/app

# Create docker-compose.yml
echo "Creating docker-compose.yml..."
cat <<EOT > docker-compose.yml
version: '3'
services:
  backend:
    image: abdulraheem381/todo-backend:latest
    container_name: todo-backend
    ports:
      - "5000:5000"
    networks:
      - todo-network

  frontend:
    image: abdulraheem381/todo-frontend:latest
    container_name: todo-frontend
    ports:
      - "5173:5173"
    networks:
      - todo-network

networks:
  todo-network:
    driver: bridge
EOT

if [ -f "docker-compose.yml" ]; then
    echo "docker-compose.yml created successfully."
else
    echo "Error: docker-compose.yml was NOT created."
    exit 1
fi

# Pull latest images and start containers
echo "Starting containers..."
sudo docker compose pull
sudo docker compose up -d

echo "User data script execution completed."
