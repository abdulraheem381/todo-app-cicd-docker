

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

  user_data = file("${path.module}/user_data.sh")

  tags = {
    Name = "Todo-App-Instance"
  }
}