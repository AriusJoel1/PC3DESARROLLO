# infra/terraform/main.tf
terraform {
  required_version = "~> 1.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-west-2"
}

module "example" {
  source         = "./modules/example_module"
  instance_count = 1
}

resource "aws_security_group" "allow_ssh_bad" {
  name = "bad-ssh"
  ingress {
    from_port   = 22
    to_port     = 22
    cidr_blocks = ["0.0.0.0/0"]
  }
}
