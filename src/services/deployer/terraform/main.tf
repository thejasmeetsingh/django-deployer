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
  name   = format("%s Security Group", var.project_name)
  vpc_id = aws_default_vpc.default_vpc.id
}

resource "aws_vpc_security_group_egress_rule" "deployer_sg_outbound" {
  security_group_id = aws_security_group.deployer_sg.id
  ip_protocol       = "-1"
  cidr_ipv4         = "0.0.0.0/0"
}

resource "aws_vpc_security_group_ingress_rule" "deployer_sg_inbound_http" {
  description       = "HTTP Inbound Rule"
  security_group_id = aws_security_group.deployer_sg.id
  from_port         = 80
  to_port           = 80
  ip_protocol       = "tcp"
  cidr_ipv4         = "0.0.0.0/0"
}

resource "aws_vpc_security_group_ingress_rule" "deployer_sg_inbound_https" {
  description       = "HTTPS Inbound Rule"
  security_group_id = aws_security_group.deployer_sg.id
  from_port         = 443
  to_port           = 443
  ip_protocol       = "tcp"
  cidr_ipv4         = "0.0.0.0/0"
}

resource "aws_instance" "deployer_vm" {
  ami                         = data.aws_ami.ubuntu_ami.id
  instance_type               = var.instance_type
  associate_public_ip_address = true
  subnet_id                   = aws_default_subnet.default_subnet.id
  vpc_security_group_ids      = [aws_security_group.deployer_sg.id]
  user_data                   = templatefile("./instance.init.sh", { project_link = "${var.project_link}" })

  ebs_block_device {
    device_name = "/dev/sda1"
    volume_size = 8
    volume_type = "gp2"
  }

  tags = {
    Name = format("%s VM", var.project_name)
  }
}

resource "aws_eip" "deployer_eip" {
  instance = aws_instance.deployer_vm.id

  tags = {
    Name = format("%s VM Elastic IP", var.project_name)
  }
}

output "instance_dns" {
  description = "Instance Public IPv4 DNS"
  value       = aws_eip.deployer_eip.public_dns
}
