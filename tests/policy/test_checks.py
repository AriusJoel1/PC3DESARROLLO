import pytest
from policy import checks

GOOD_TF = '''
resource "aws_security_group" "good-ssh" {
  name = "good-ssh"
  ingress {
    from_port = 443
    to_port   = 443
    cidr_blocks = ["10.0.0.0/24"]
  }
}
'''

BAD_TF_PORT = '''
resource "aws_security_group" "bad-SSH" {
  name = "Bad_SSH"
  ingress {
    from_port = 22
    to_port   = 22
    cidr_blocks = ["0.0.0.0/0"]
  }
}
'''

BAD_TF_SECRET = '''
variable "db_password" {
  default = "SuperSecret123!"
}
'''


@pytest.mark.parametrize("content,expect_findings", [
    (GOOD_TF, False),
    (BAD_TF_PORT, True),
    (BAD_TF_SECRET, True),
])
def test_run_all_checks_on_text_simple(content, expect_findings):
    findings = checks.run_all_checks_on_text(content)
    has_findings = len(findings) > 0
    assert has_findings == expect_findings


def test_evaluate_files_io(tmp_path):
    # create temp file
    p = tmp_path / "tmp.tf"
    p.write_text(BAD_TF_PORT)
    res = checks.evaluate_files([str(p)])
    assert str(p) in res
    assert any(f.get("type") == "common_insecure_port" or f.get("type") == "insecure_bind" for f in res[str(p)])


@pytest.mark.xfail(reason="policy: future check for header metadata required", strict=False)
def test_future_policy():
    # Placeholder test for a policy planned in next sprint
    assert False
