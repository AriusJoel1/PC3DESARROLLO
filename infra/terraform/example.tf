# Ejemplo vulnerable (insecure) y ejemplo bueno

# --- vulnerable security group (insecure) ---
resource "aws_security_group" "bad-SSH" {
  name = "Bad_SSH" # bad naming (uppercase & underscore)
  ingress {
    from_port   = 22
    to_port     = 22
    cidr_blocks = ["0.0.0.0/0"]
  }
  # secret accidentally included:
  aws_access_key_id = "AKIAEXAMPLEKEY1234"
}

# --- good example ---
resource "aws_security_group" "good-ssh" {
  name = "good-ssh"
  ingress {
    from_port   = 443
    to_port     = 443
    cidr_blocks = ["10.0.0.0/24"]
  }
}
