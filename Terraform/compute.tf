

resource "aws_instance" "main" {
  ami                         = "ami-019715e0d74f695be"
  instance_type               = "t2.micro"
  availability_zone           = "ap-south-1a"
  associate_public_ip_address = true
  vpc_security_group_ids      = [aws_security_group.todo_sg.id]

  root_block_device {
    volume_type = "gp3"
    volume_size = 20
  }

  user_data = <<-EOF
    #!/bin/bash
    set -e

    # Update system and install Docker
    apt update -y
    apt install -y docker.io docker-compose-plugin

    # Enable and start Docker
    systemctl enable docker
    systemctl start docker
    usermod -aG docker ubuntu

    # Create app directory
    mkdir -p /home/ubuntu/app
    cd /home/ubuntu/app

    # Create docker-compose.yml
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

    # Pull latest images and start containers
    docker compose pull
    docker compose up -d
  EOF

  tags = {
    Name = "Todo-App-Instance"
  }
}