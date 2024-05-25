data "aws_ami" "ubuntu_ami" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["ubuntu/images/hvm-ssd/ubuntu-jammy-22.04-amd64-server-*"]
  }

  filter {
    name   = "virtualization-type"
    values = ["hvm"]
  }
}

data "template_file" "instance_init" {
  template = file("../instance.init.sh")

  vars = {
    arg1 = var.project_path
    arg2 = var.project_name
  }
}
