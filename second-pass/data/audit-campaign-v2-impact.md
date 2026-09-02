# Campaign amendment v2 — retroactive impact statement

Date: 2026-07-30. Amendment: two verdict-mapping exceptions added to
`prompts/audit.md` (documented supplied-model representation gaps and
canonical-vs-docstring contradictions map to `CONCERNS / LEGIT`). The v1
lock is preserved at `data/audit-campaign.v1.lock.json`.

Scanned every completed selected `FAIL` audit in both finished arms for
verdicts that could flip under the amendment:

- Bare arm: 100 FAIL selections scanned — **no flips**. Exception (1) is
  structurally inapplicable (no supplied reference semantics exists in
  that arm; every representation gap is in the candidate's own generated
  theory). Every canonical-related contradiction has the candidate
  diverging from canonical, the opposite of the protected shape.
- Semantics arm: 91 FAIL selections scanned — **no flips**. Every FAIL is
  an overclaim (theorem false on a concrete witness) or candidate-caused
  narrowing, both explicitly excluded by the amendment. The two
  documented-boundary trust-ledger cases (0, 64) fail on independent
  Gate A false-bridge defects that the reviewer ruled decisive.

Conclusion: the amendment changes no completed verdict in any arm. It
governs only future kit-semantics audits under the v2 lock
(`bare-semantics-audit-20260726+kitsem-v2-20260730`).
