# Ejemplo Rego para futura integración con OPA/Conftest
package terraform.security

deny[msg] {
  input.resource[_].ingress[_].from_port == 22
  msg := sprintf("SSH open to 0.0.0.0 (port 22) in resource %v", [input.resource[_].name])
}
