# Proven-versus-assumed ledger

## Formally established by the reconstructed K proof

For every `N:Int`, from the exact entry configuration in `spec.k`, the supplied
MPY semantics executes the constructor-identical translated module and call,
terminating with `<k> N *Int N </k>`. The module scope contains the expected
closure, while `env`, `scopeLoc`, `heap`, `heapLoc`, `stack`, `ret`, `exc`, and
`exit-code` have the exact final values stated by the claim.

There are no proof-local functions, rules, lemmas, simplifications, opaque
symbols, or operational bridges in `verification.k`.

## Opaque fixed-semantics symbols

The exhaustive inventory identifies 25 declarations carrying `symbol(...)`.
None is reachable from this program or its claim:

- `md5hexCodes`
- `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`
- `floorFI`, `toF`, `ceilF`
- `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`
- `decStrToF`, `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`,
  `sqrtF`
- `sortVS`, `sortKeyVS`

Twenty-two also carry `no-evaluators`; `floorFI`, `toF`, and `ceilF` have only
concrete equations and are likewise opaque on symbolic proof inputs. Their
unreachability follows from the submitted constructor set
`Module/FuncDef/Params/Return/BinOp("*")/Name` plus the entry `Call/Int`.

Other off-path total-but-partially-equated helpers (for example `valSeqAt` on
an opaque or out-of-bounds sequence) are fixed-semantics subset boundaries.
No such helper occurs in the target path or postcondition.

## Trusted primitives and assumptions

- The byte-identical supplied `reference-semantics` tree is the selected
  language model. The target depends specifically on module loading, scope
  lookup/maps, function frames/parameter binding/return, K sequencing,
  integer values, and K integer multiplication.
- K v7.1.293, the Haskell/LLVM backends, K's builtin mathematical integer,
  map/list/string theories, and the prover/solver implementation are trusted.
- CPython's parser/AST and the trusted `py2mpy.py` transliterator are trusted
  for source-to-constructor translation. For the used nodes, inspection shows
  direct mappings for module, function definition, parameter (annotation
  ignored), return, multiplication, and name; regeneration is byte-identical.
- The trusted canonical Python program is an executable differential oracle.
  Its `n ** 2` equals candidate `n * n` for mathematical/Python integers.
- The road-model connection is informal ordinary combinatorics: with unchanged
  trajectories, each of the `n` cars in one direction meets each of the `n`
  cars in the other direction exactly once, giving `n × n` collisions.

## Empirical evidence and exclusions

The 968-case differential test has zero mismatches and supports—but does not
replace—the source/canonical bridge. Fresh LLVM runs support the used
source-semantics execution path but do not prove the entire MPY language.

The theorem excludes non-integer dynamic Python arguments, total-correctness of
arbitrary programs, and all unused MPY constructs. A physical interpretation
of negative car counts is excluded, though the implementation theorem is
stronger and covers every K integer.
