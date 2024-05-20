terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

resource "aws_vpc" "deployer_vpc" {
  cidr_block = "172.31.0.0/16"
}

resource "aws_security_group" "deployer_sg" {
  name   = "Deployer Security Group"
  vpc_id = aws_vpc.deployer_vpc.id
}

resource "aws_vpc_security_group_egress_rule" "deployer_sg_outbout" {
  security_group_id = aws_security_group.deployer_sg.id
  from_port         = 0
  to_port           = 0
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

  vpc_security_group_ids = [aws_security_group.deployer_sg.id]

  ebs_block_device {
    device_name = "deployer_vm_ebs"
    volume_size = 10
    volume_type = "gp2"
  }

  tags = {
    Name = "deployerVM"
  }
}
