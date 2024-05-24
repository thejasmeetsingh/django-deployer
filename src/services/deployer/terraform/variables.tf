variable "instance_type" {
  description = "AWS Instance Type"
  type        = string
  default     = "t2.micro"
}

variable "az" {
  description = "AWS Subnet Availability Zone"
  type        = string
  default     = "ap-south-1b"
}
