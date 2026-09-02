# Evidence index

- `00`–`07`: launcher mode, mounted files, producer-source hashes, accessible
  provenance/tree hashes, trusted-tool source, and toolchain metadata.
- `08`: raw first inventory reconstruction. Its `ORDERED_IDENTITY_BIJECTION`
  diagnostic is false because it incorrectly projected source fields that the
  compact Stage 3 schema does not duplicate.
- `09`: corrected authoritative comparison using ordered IDs, uniqueness, the
  whole inventory hash, and `validate_trust_boundary`; every check passes.
- `10`–`11`: frozen operational semantics and independent classifications.
- `12`–`18`: preflight attempt, PID-namespace diagnosis, narrow runtime shim,
  frozen-toolchain gate, and successful trusted preflight rerun.
- `19`–`23`: generated/candidate sources, integer-sort bindings, target-hash
  machinery, and independent obligation/target reconstruction.
- `24`–`26`: fresh proof copy, exact `Base` tree match, mandatory `lake clean`
  and `lake build`, candidate static gate, and target identity.
- `27`–`29`: exact `#print axioms Proof.final`, trusted final mechanical gate,
  and axiom reconciliation.
- `30`–`31`: adversarial operational-bridge tests, counterfactual mutations,
  compiled KORE hook identities, frozen source, and exact candidate bindings.
- `32`: launcher resolution hash and generator/toolchain-lock clarification.
