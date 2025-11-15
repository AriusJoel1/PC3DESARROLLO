from policy import checks

SAMPLE_GOOD = """
resource "aws_security_group" "good" {
  name = "good-ssh"
  ingress {
    from_port = 443
    to_port   = 443
    cidr_blocks = ["10.0.0.0/24"]
  }
}
"""

SAMPLE_BAD = """
resource "aws_security_group" "bad-SSH" {
  name = "Bad_SSH"
  ingress {
    from_port = 22
    to_port   = 22
    cidr_blocks = ["0.0.0.0/0"]
  }
}
variable "db_password" {
  default = "SuperSecret123!"
}
"""


def test_policy_detects_bad_and_good(tmp_path):
    g = checks.run_all_checks_on_text(SAMPLE_GOOD)
    assert len(g) == 0

    b = checks.run_all_checks_on_text(SAMPLE_BAD)
    assert any(
        f["type"] in ("insecure_bind", "common_insecure_port", "secret", "naming")
        for f in b
    )
