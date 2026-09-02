# Stage 4 producer-source bundles

This directory freezes the exact Stage 4 producer sources used by the final
selected HumanEval bare and with-semantics generations. Each digest-named
directory corresponds to one immutable generator image and contains:

- `klean.py`
- `klean_export.py`
- `source-manifest.json`, which authenticates the files and generator image

Stage 6 mounted the bundle matching each selected Stage 4 generation read-only
at `/reference/generation-tools`. These bundles therefore record which source
code produced each audited Lean target; they are not proof candidates or one
directory per benchmark case.

## Final portfolio

The active directory contains 13 referenced producer bundles covering all 137
selected Stage 4 cases:

- 64 bare cases
- 73 with-semantics cases
- 28 `PASS` cases covering 51 Lean proof obligations
- 109 `KLEAN_NO_OBLIGATIONS` classification-only cases

Ten producer versions are used by at least one proof-producing case. Three
additional versions are used only by selected classification-only cases, so
they remain required provenance.

See [`index.json`](index.json) for the exact mapping from generator digest to
arm, task, selected generation, Stage 4 status, and obligation count.

## Retention rule

A bundle stays in this directory if at least one final
`04-klean-generation/selected.json` resolves to a generation whose
`generator-manifest.json` records that image digest. Do not rename or move an
active bundle: completed audit inputs record its path and hashes.

Bundles with zero final selections are moved to
[`legacy/stage4-producer-sources`](../../legacy/stage4-producer-sources) rather
than mixed with active evidence. The archived digests are also recorded in
`index.json`.
