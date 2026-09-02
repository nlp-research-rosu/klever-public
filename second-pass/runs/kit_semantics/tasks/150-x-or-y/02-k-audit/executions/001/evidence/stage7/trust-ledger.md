# Proven/assumed ledger

## Components on the theorem's dependency path

| Component | Role | Dependents | Status |
|---|---|---|---|
| Supplied `MPY` rules for module loading, statement sequencing, ordinary name lookup/assignment, calls, frames, return, `If`, `While`, integer comparison/arithmetic, and Python modulo | Gives meaning to every material operation in the literal submitted constructor body | Both reachability claims | Trusted fixed semantics, statically checked against the used Python behavior and exercised by fresh LLVM probes |
| K built-ins `Int`, `Bool`, `Map`, `List`, equality, integer `+`, comparison, remainder, and division | Mathematical/data-structure substrate of MPY and `trialChoice` | Semantics and summaries | Standard K primitive trust boundary; no replacement of program-defined code |
| K v7.1.293 parser, kompiler, Haskell backend, Kore prover, and generated strictness machinery | Builds and checks the reachability proof | Fresh `#Top` results | Toolchain trust boundary |
| `trialChoice` equations | Defines the remaining divisor scan | Loop and entry claims | Proved-connected definitional summary; guarded, disjoint, exhaustive on every occurrence, and terminating on ground used instances |
| `xOrYSpec` equations | Splits `N < 2` from the scan | Entry postcondition | Fully defined over `Int × Val × Val`; guarded, disjoint, and exhaustive |
| `[trial-loop]` reachability claim | Universal bridge from the real fixed-semantics loop to `trialChoice` | Entry claim | Machine-checked circularity; not an assumed operational rewrite |
| Trusted `py2mpy.py` | Source-to-constructor bridge | Program-identity conclusion only | Byte-identical regeneration plus parsed-constructor comparison; not a premise of the K reachability derivation |

There is no proof-local trusted primitive, operational bridge, priority rule,
simplification, opaque result oracle, or empirical axiom.

## Imported but dependency-disjoint opaque/total boundaries

The Haskell definition imports the complete supplied MPY module. The following
supplied symbols are opaque for symbolic proof (`no-evaluators`) and have
concrete LLVM twins or an explicit external contract:

- Float/conversion family:
  `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`, `subF`, `divF`,
  `addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`, `divFloatIntV`,
  `intToF`, `truncF`, `roundF`, `roundFN`, and `sqrtF`.
- Sorting family: `sortVS` and `sortKeyVS`.
- Digest family: `md5hexCodes`.

`floorFI`, `toF`, and `ceilF` are also effectively opaque on symbolic
arguments because their defining equations are `[concrete]`. The compiler
additionally warns that supplied total helpers `mapStrVS`, `floorFI`, `toF`,
`ceilF`, `joinCodes`, and `valSeqAt` are non-exhaustive on unrelated constructor
cases.

None of these symbols, their routing rules, floats, containers, sorting,
hashing, methods, slicing, comprehensions, or builtins occurs in the submitted
program term, either summary, or either reachability configuration. They
therefore do not fix a task result, choose a task branch, or replace task
execution. They remain limitations of the broad supplied semantics, not
assumptions supporting this theorem.

The `MPY-CONCRETE` module is included only in the fresh LLVM runtime definition.
It is not imported by `VERIFICATION`.

## Empirical and informal bridges

- `differential.py` compares the trusted canonical Python entry point with the
  candidate over 624 cases. This is finite evidence only. It finds agreement
  for every tested `n >= 1` and a systematic disagreement for `n <= 0`.
- `concrete_probe.py` runs ten ground executions in freshly compiled LLVM MPY,
  including negative, zero, prime, and composite cases. This checks execution
  plumbing, not the universal theorem.
- `ground_witnesses.py` evaluates concrete substitutions of the formal summary
  against both Python implementations. Again this is finite evidence.
- The informal intent bridge is the elementary number-theoretic fact that for
  `N >= 2`, absence of a divisor in the complete range `2 .. N-1` is equivalent
  to primality. The recurrence itself and its connection to execution are
  formal; calling that condition “prime” is the human-facing interpretation.
- The prompt says “prime” versus “otherwise” without an explicit positivity
  precondition. The trusted canonical's behavior at `n <= 0` conflicts with
  that ordinary mathematical reading. This boundary disagreement is not used
  to establish `#Top`; it is an intent/provenance concern.
