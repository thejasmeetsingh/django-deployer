terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

resource "aws_default_vpc" "default_vpc" {
  tags = {
    Name = "Default VPC"
  }
}

resource "aws_default_subnet" "default_subnet" {
  availability_zone = var.az
}

resource "aws_security_group" "deployer_sg" {
  name   = "Deployer Security Group"
  vpc_id = aws_default_vpc.default_vpc.id

  egress = [{
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }]

  ingress = [
    {
      from_port   = 80
      to_port     = 80
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    },
    {
      from_port   = 443
      to_port     = 443
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
    }
  ]
}

resource "aws_instance" "deployer_vm" {
  ami                         = data.aws_ami.ubuntu_ami.id
  instance_type               = var.instance_type
  associate_public_ip_address = true
  subnet_id                   = aws_default_subnet.default_subnet.id
  security_groups             = [aws_security_group.deployer_sg.name]

  ebs_block_device {
    device_name = "/dev/sda1"
    volume_size = 8
    volume_type = "gp2"
  }

  tags = {
    Name = "Deployer VM"
  }
}

resource "aws_eip" "deployer_eip" {
  instance = aws_instance.deployer_vm.id
}
