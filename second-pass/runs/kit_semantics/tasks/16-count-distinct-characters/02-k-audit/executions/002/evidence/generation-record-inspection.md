# Generation-record inspection (untrusted evidence)

Declared layout: `pipeline-v3`. All required records were present as regular
files/directories:

- `/run.json`, `/task.json`, `/generation-result.json`
- `/generation-evidence/invocation.json`
- `/generation-evidence/metrics.json`
- `/generation-evidence/runtime-metrics.json`
- `/generation-evidence/usage.json`
- `/generation-evidence/codex-last.txt`
- `/generation-evidence/codex-output.log`
- `/generation-evidence/prompt.txt`
- `/generation-evidence/codex-trace/`

The exact SHA-256 values are in `stage1-provenance.log` and match the values
recorded by `/audit-input.json` and `/generation-result.json`, including the
single trace JSONL file hash. The structured trace has 221 valid JSON events:
154 response items, 64 event messages, one session metadata record, one world
state, and one turn context. Its response items contain 55 reasoning records,
29 custom tool calls plus 29 outputs, 15 messages, and 13 function calls plus
13 outputs. The flattened `codex-output.log` has 17,160 lines.

The untrusted records claim that generation:

1. read Kit material and relevant semantics;
2. wrote the canonical `len(set(string.lower()))` implementation;
3. built LLVM and Haskell definitions;
4. obtained `#Top`;
5. ran candidate-authored off-by-one and body mutations;
6. ran finite Python tests and a U+0130 model-gap witness; and
7. reported `VALIDATED` / `KPROVE_PASSED`.

The raw flattened log and structured event sequence were inspected for the
actual commands and outputs. They include the claimed successful `kompile`,
`krun`, and `kprove` calls, the two candidate mutation failures, later repeated
end-to-end runs, and one irrelevant failed attempt to invoke unavailable
`git`. None of those generation claims was used as proof evidence in the
verdict: the audit regenerated, rebuilt, reproved, and remutated independently.
