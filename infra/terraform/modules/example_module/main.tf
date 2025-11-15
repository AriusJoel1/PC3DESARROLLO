variable "instance_count" {
  type    = number
  default = 1
}

resource "aws_instance" "vm" {
  count         = var.instance_count
  ami           = "ami-12345678"
  instance_type = "t3.micro"
  tags = {
    Name = "example-${count.index}"
  }

  root_block_device {
    encrypted = true
  }

  metadata_options {
    http_tokens = "required"
  }
}