# Proven-versus-assumed ledger

## Machine-checked result

Under the supplied `MPY` proof definition, for every finite `ValSeq VS` whose
elements are `Int` or `Float`:

1. The loop circularity starts at the actual
   `#loop(list(VS), Name("grade"), GRADE-STEP)` control point with an existing
   output list `ACC`. If execution terminates, it preserves framed control and
   state, leaves the output heap object containing `gradeAcc(ACC, VS)`, and
   permits only the local loop variable's final value to vary.
2. The entry claim starts at the complete initial MPY state, loads the exact
   submitted module constructor term, resolves and invokes
   `numerical_letter_grade`, and, if execution terminates, returns `ref(0)` to
   the sole heap object `list(gradeAcc(.ValSeq, VS))` with no exception and
   exit code 0.

`gradeAcc` preserves order and emits exactly one `gradeValue` per input.
`gradeValue` is the submitted descending threshold chain expressed in the
fixed semantics' `eqF`/`gtF` comparison primitives.

The proof does not establish a separate termination theorem.

## Trusted or informal boundaries

| Boundary | Value/control/state influence | Dependents | Evidence and disposition |
|---|---|---|---|
| Supplied MPY operational semantics | Defines all syntax, control, lookup, frames, allocation, list iteration/mutation, and return behavior | Both claims | Launcher-trusted input; candidate copy is entry/type/byte identical. The used path was statically reviewed and concretely executed. Acceptable selected-semantics boundary. |
| `intToF`, `eqF`, `gtF`, and K Float hooks (`Int2Float`, `==Float`, `>Float`) | Determine every comparison atom, branch, and output letter | `gradeEq`, `gradeGt`, `gradeValue`, loop and entry | Fixed primitives in trusted `float.k`, with LLVM `[concrete]` equations; proof is interpretation-parametric. LLVM boundary smoke and 2,048-case Python differential support the intended interpretation. Acceptable low-level boundary, but not a theorem of IEEE arithmetic inside Haskell `kprove`. |
| K parser/compiler/Haskell prover/LLVM runtime | Checks reachability and executes concrete semantics | All formal/dynamic evidence | Version 7.1.293, rebuilt from source in scratch. Standard trusted toolchain boundary. |
| Trusted `py2mpy.py` translator | Determines the submitted constructor program | Program identity and both claims | Candidate translator matches trusted hash; trusted regeneration is byte-identical; expanded proof macro equals regenerated term. Translator correctness itself is trusted. |
| Trusted prompt and canonical implementation | Define source intent and independent Python oracle | Adequacy and differential checks | Prompt/canonical hashes match launcher records. Candidate and canonical agree on 2,048 recorded cases. They are not K proof axioms. |
| Bare `list(VS)` symbolic input representation | Avoids allocating a caller-owned input heap object; the function only reads it | Entry scope and allocation location (`ref(0)`) | Explicitly supported by fixed `core.k` for read-only proof inputs. The submitted function neither mutates nor returns the input. Concrete allocated-list execution and Python comparison agree. Acceptable representation bridge for the requested return-value property. |
| ASCII `strToCodes` model | Represents output grade strings | `gradeValue`, heap postcondition | Every output is ASCII; fixed `str.k` equations are exact on these literals. Acceptable. |
| Termination | Reachability result is partial correctness | Both claims | Not assumed to obtain a total-correctness theorem. Finite constructor sequences and concrete runs support termination, but the report does not elevate this to a separate proof. |

There are no proof-local opaque symbols, trusted primitives, operational
bridges, arbitrary result generators, or answer axioms. Differential and LLVM
tests support only the listed semantic/intent bridges and are not substitutes
for the symbolic reachability proof.
