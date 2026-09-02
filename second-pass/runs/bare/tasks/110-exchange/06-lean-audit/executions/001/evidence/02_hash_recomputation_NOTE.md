The `audit_input_contract_verified: false` field in
`02_hash_recomputation.log` is a diagnostic-wrapper mistake: that command
compared the resolution object returned by `verify_stage6_audit_input` with
the entire audit-input envelope. It is not a contract failure.

`12_audit_input_contract.log` performs the correctly typed comparison
(`returned resolution == document["resolution"]`) and records `true`, along
with the exact recomputed envelope digest.
