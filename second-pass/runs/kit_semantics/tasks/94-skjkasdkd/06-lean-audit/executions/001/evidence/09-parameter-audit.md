# Independent Stage 5 parameter audit

The generated target has 21 parameters. The trusted mechanical gate found
exactly one candidate `def` for each parameter and verified that
`Proof.final` applies those exact definitions to the immutable generated
target. The following judgment is semantic, not inferred from the clean build.

| Target parameter | Candidate definition | Frozen meaning and audit judgment |
|---|---:|---|
| `«_-Int_»` | `Proof.lean:97` | `x - y`; matches K integer subtraction. |
| `_andBool_` | `Proof.lean:99` | `x && y`; matches strict K Boolean conjunction on the complete Bool domain. |
| `«_>Int_»` | `Proof.lean:101` | Decidable integer `>`; matches the K hook. |
| `«_>=Int_»` | `Proof.lean:103` | Decidable integer `>=`; matches the K hook. |
| `«_<Int_»` | `Proof.lean:105` | Decidable integer `<`; matches the K hook. |
| `«_<=Int_»` | `Proof.lean:107` | Decidable integer `<=`; matches the K hook. |
| `«_==Int_»` | `Proof.lean:109` | Decidable integer equality; matches the K hook. |
| `«_=/=Int_»` | `Proof.lean:111` | Decidable integer inequality; matches the K hook. |
| `«_%Int_»` | `Proof.lean:113` | **Mismatch.** Frozen KORE declares this symbol with `hook("INT.tmod")`; the candidate uses Lean `%`, which is `Int.emod`. For `(-5, 3)`, frozen K evaluates to `-2`, while the candidate evaluates to `1`. This is a total, adversarial witness in the target parameter's declared `SortInt → SortInt → SortInt` domain. |
| `«_+Int_»` | `Proof.lean:115` | `x + y`; matches K integer addition. |
| `«_/Int_»` | `Proof.lean:117` | `Int.tdiv x y`; matches frozen `hook("INT.tdiv")` wherever the K hook is defined. |
| `«applyBin(_,_,_)_MPY-CORE_Val_String_Val_Val»` | `Proof.lean:119` | The source-linked integer `+` and Python `%` branches agree with their two local rules. **The bound KORE symbol as a whole is not implemented:** all non-integer/Boolean cases and some integer operators fall to `noneV`. In particular, supplied `float.k:32` rewrites `applyBin("/", 1, 2)` to `divII(1,2)`, whereas the candidate returns `noneV`. |
| `«applyCmp(_,_,_)_MPY-CORE_Bool_String_Val_Val»` | `Proof.lean:134` | The three source-linked integer order comparisons are correct. **The bound KORE symbol as a whole is incomplete:** supplied semantics also defines Float, String, list, tuple, set, dictionary, and `noneV` comparison cases; the candidate returns `false` outside its integer/Boolean projection. |
| `«definedProjectInt(_)_VERIFICATION_Bool_Val»` | `Proof.lean:147` | True exactly for the `SortVal.inj_SortInt` constructor, matching the fresh Stage 1 definition `definedProjectInt(V) => isInt(V)`. |
| `«digitSum(_)_VERIFICATION_Int_Int»` | `Proof.lean:150` | Uses a terminating recurrence with base `n <= 0 ↦ 0` and the exact positive `pyMod`/truncating-division step; matches frozen lines 167–173. Boundary checks `0`, `1`, `10`, `181`, and negative inputs follow the recurrence. |
| `isInt` | `Proof.lean:153` | Recognizes exactly a singleton K sequence whose item is an injected Int. This matches the generated sort predicate in every target use. |
| `«primeTail(_,_)_VERIFICATION_Bool_Int_Int»` | `Proof.lean:156` | Matches all three frozen defining cases: `d < 2 ↦ false`, `d >= n ↦ true`, and the nondivisibility recurrence for `2 <= d < n`. |
| `«project:Int»` | `Proof.lean:159` | Returns the injected Int on the partial projector's defined domain. The `0` default is outside that K projector's defined domain and is never admitted by the corresponding guarded obligation. |
| `projectIntTotal` | `Proof.lean:162` | Returns the Int payload on the Stage 1 definition's guarded domain and chooses `0` for otherwise-unfixed totalization cases. It satisfies the primary definition and the exact linked idempotence use. |
| `«pyMod(_,_)_MPY-INT_Int_Int_Int»` | `Proof.lean:165` | `((n % d) + d) % d`; on every nonzero divisor this equals the supplied `pyMod` rule `((n %Int d) +Int d) %Int d`, even though Lean `%` and K `%Int` differ before normalization. All linked uses have positive divisors. |
| `«project:Int?»` | `Proof.lean:168` | `some i` exactly on a singleton K sequence containing injected Int `i`, and `none` otherwise; matches the optionalized partial cast. |

## Adversarial and counterfactual evidence

`08-operational-bridge-probes.out` records:

- the compiled KORE declaration binding `«_%Int_»` to `INT.tmod`;
- live K evaluation `-5 %Int 3 = -2`;
- live Lean evaluation `Proof.«_%Int_» (-5) 3 = 1`,
  `Int.tmod (-5) 3 = -2`, and `Int.emod (-5) 3 = 1`;
- agreement on the convenient positive witness `17 % 10 = 7`, showing why
  the generated positive-digit obligations do not expose the mismatch;
- the candidate returning `noneV` for integer true division even though the
  supplied semantics has an ordinary `divII` execution rule; and
- a counterfactual candidate changing that unmodeled integer-division result
  to the hard-coded integer `999`. `lake clean` and `lake build` still pass
  and `Proof.final` remains provable. This demonstrates that the theorem
  constrains only the source-linked branches and cannot by itself validate
  the whole bound `applyBin` implementation.

The `«_%Int_»` witness alone is an operational-bridge failure under the audit
instruction requiring every target parameter to implement its frozen
operational meaning. The two whole-symbol dispatch incompletenesses provide
additional independent failures.
