# Portable CI Kernel — local review candidate

This is a dependency-free demonstration of a fail-closed classifier for change records.

Run on Windows or Linux:

```
python -m unittest discover -s tests -v
```

## Security scope

The default policy is **synthetic**, not CarpetAI's private governance policy.
A GREEN outcome means *only* that paths, change status and patch presence
matched the demonstration allowlist. **Do not use GREEN to authorize merges.**
The classifier does not currently inspect added-line semantics or prove that
the submitted patch corresponds to the real Git diff. Inputs and caller
configuration must be trusted; it is not a security boundary for hostile PRs.

The GitHub Actions workflow uses standard Ubuntu and Windows runners with
read-only repository permissions. No private checkout or credentials are needed.

## Publication gate

Not published. This repository has fresh history and must not receive private
Git history, credentials, customer data, proprietary supplier information or
private policy. Public disclosure requires an exact-commit independent review,
license selection and explicit owner approval.

Public module tests never replace private CarpetAI CI, independent review or
its official merge gate.
