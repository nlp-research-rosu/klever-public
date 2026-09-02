# Audit evidence index

All commands were run against fresh sources under
`/tmp/audit-work/79-decimal-to-binary`. Every numbered log starts with the
exact shell-escaped command and ends with `EXIT_STATUS`.

- `01`–`03`: provenance, trusted translation identity, and Python differential.
- `04`–`08`: fresh concrete/proof builds, concrete runs, and the candidate
  positive `#Top`.
- `09`: an auditor-authored full-module claim with an intentionally incomplete
  post-state; it correctly exposes the retained module binding.
- `10`–`11`: corrected full-module `#Top` and concrete formal-result witnesses.
- `12`, `12b`: superseded inventory formatting passes; `12c` and the current
  TSV files are authoritative.
- `13`: bridge-free fixed-semantics proof build.
- `14`: a rejected functional-claim encoding unsupported by this Haskell
  backend; `14b` is the correctly configured ground connection proof.
- `15`: the meaningful stuck universal bridge-free slice connection.
- `16`–`17`: extension ground agreement and rejection of an opposite slice
  result.
- `18`: fresh false-postcondition mutation, rejected on the expected
  result-character obligation.
- `19`–`20`: tool versions and source hashes.
- `21`: final review/evidence consistency validation.

Reviewer-authored executable sources are preserved alongside the logs. The
complete statement inventory is `k-rule-inventory.tsv`; the row-level local
review is `k-rule-review.tsv`.
