# infra/terraform/modules/example_module/main.tf
variable "instance_count" {
  type    = number
  default = 1
}

resource "aws_instance" "vm" {
  count = var.instance_count
  ami           = "ami-12345678"
  instance_type = "t3.micro"
  tags = {
    Name = "example-${count.index}"
  }
}
