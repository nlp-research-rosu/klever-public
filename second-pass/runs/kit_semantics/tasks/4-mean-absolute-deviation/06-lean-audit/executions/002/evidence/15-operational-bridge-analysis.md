# Operational-bridge analysis

The six target parameters were compared with the bound KORE symbol, all bound
source-rule IDs, the frozen `verification.k`, `solution.py`, and the supplied
semantics. Candidate line numbers below refer to `/candidate/Proof.lean`.

| Parameter | Frozen operational meaning on its bound obligations | Candidate definition | Judgment |
|---|---|---|---|
| `addF` / `LbladdF` | `float.k` declares `addF(Float,Float)` and its concrete rule reduces to K `+Float`; the supplied `applyBin("+", Float, Float)` rule dispatches to it. | Lines 39–40 use Lean `Float.add` on `SortFloat = Float`. | Exact on all inputs. |
| `applyBin` / `LblapplyBin…` | Rule `92241e…` needs `applyBin("+", inj A, V)` with `isFloat(V)`; rule `6f2599…` needs `applyBin("-", V, inj M)` with the same guard. The supplied typed dispatches produce `inj (addF A F)` and `inj (subF F M)`. | Lines 71–76 map Float/Float subtraction and addition to `Float.sub` and `Float.add`; the guard model below forces `V` to the Float constructor. | Exact on the complete match domains of both bound rules. Other numeric branches implement additional supplied dispatches; the default is outside these obligations. |
| `isFloat` / `LblisFloat` | The K sort predicate is true exactly for the Float injection. In the generated call shape it receives `kseq (inj V) dotk`. | Lines 9–11 recognize exactly `kseq (inj_SortFloat value) dotk`; lines 102–103 return its `isSome`. | Exact; non-Float and malformed/continued K sequences are false. |
| `projectFloat` / `LblprojectFloat` | Frozen defining rules make it the identity on a `Float` value; all uses in the two domain lemmas are guarded by `isFloat`. Its `[total]` value outside that guard is not fixed by any equation. | Lines 106–108 return the Float payload and choose an arbitrary inhabitant only outside the guarded domain. | Exact on every operationally relevant use; the outside-domain choice cannot affect either obligation. |
| `subF` / `LblsubF` | Concrete `subF` reduces to K `-Float`; the supplied Float subtraction dispatch uses it. | Lines 13–14 and 111–112 use Lean `Float.sub`. | Exact on all inputs. |
| `project:Float?` / `Lblproject'Coln'Float` | The KORE partial projection is `some F` exactly for a Float injection and `none` otherwise. | Lines 115–116 reuse the exact structural projection at lines 9–11. | Exact on all generated `SortK` values. |

Adversarial Lean examples in `11b-bridge-adversarial-examples-success.txt`
evaluate Float addition to `3.75`, subtraction to `3.25`, the corresponding
`applyBin` cases to the same injected results, and Int addition to `5`; the
same source also checks Float/non-Float predicate and projection cases.

Counterfactual source mutations were made only in disposable copies. Replacing
`addF` by the constant `0.0` makes the Float-add obligation fail at the final
proof (`12-counterfactual-addF-mutation.txt`). Replacing `isFloat` by constant
`true` exposes every non-Float constructor as a counterexample and also breaks
the projection equivalence (`13-counterfactual-isFloat-mutation.txt`). These
failures show that the submitted definitions are not accepted merely because
they are constant, identity, hard-coded, or vacuous.

This is a local bridge judgment over the emitted Lean datatypes only. It does
not repair the Stage 4 carrier loss documented in
`17-stage4-carrier-projection.txt`: because generated `SortVal` omits frozen K
string values, even honest parameter definitions and an exact proof of the
emitted declaration prove only the weakened generated theorem.
