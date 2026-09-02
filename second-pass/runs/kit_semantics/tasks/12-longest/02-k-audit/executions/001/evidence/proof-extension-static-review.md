# Proof-extension static review

This review was reconstructed from `verification.k`, `spec.k`, and
`connection-spec.k`; candidate prose was not used as authority. The exhaustive
machine inventory is `static-rule-inventory.tsv`.

## Fixed-semantics path used by the theorem

The translated module uses these source constructors: `Module`, `ImportFrom`,
`FuncDef`, `Params`, `If`, `UnaryOp("not")`, `Name`, `Return`, `NoneVal`,
`Assign`, `Subscript`, `Int`, `For`, `Compare`, `Call`, and `CmpOp(">")`.
The target proof materially exercises:

- MPY syntax strictness/contexts for `If`, `UnaryOp`, `Assign`, `Subscript`,
  `For`, `Return`, and calls/comparisons;
- configuration, module loading, statement sequencing, scope lookup,
  builtin-scope lookup, truthiness, argument evaluation, list/string lengths,
  and structural sequence-length helpers from `core.k`;
- no-op handling of the typing-only `ImportFrom`, assignment, conditional,
  and list-loop control from `controls.k`;
- function binding, exact-arity parameter binding, return, frame pop, and
  caller restoration from `functions.k`;
- ordinary callee/argument evaluation, builtin dispatch, and closure dispatch
  from `call.k`;
- `len`/`seqLen` from `builtins.k`, list iteration from `list.k`,
  name-target binding from `tuple.k`, index-zero list access from
  `subscript.k`, unary `not` from `bool.k`, and integer `>` from `int.k`.

Evaluation is left-to-right: strictness evaluates the `if` guard and assignment
RHS, call routing evaluates the callee before arguments, `#evalArgs` evaluates
arguments in order, and comparison contexts evaluate the left and then right
operand. The actual path allocates a call scope but no heap object; the list
argument is the bare symbolic `list(ValSeq)` value in the claim. Frame pop
restores the caller environment and removes the call scope. No used rule writes
output, exceptions, or exit status.

Every fixed-semantics record not marked material in the TSV is unreachable from
this submitted constructor term. In particular, the supplied opaque float,
sort, keyed-sort, and MD5 symbols are not exercised and cannot influence this
theorem. I found no concrete or symbolic witness by which an unexercised rule
can enable a false conclusion for an intended `List[str]` input; those records
are therefore classified as unexercised rather than declared globally sound.

## `isStringValue`

- Inventory: one `[function,total]` declaration and two rules.
- Equations: the `Str` case is true; the `[owise]` `Val` case is false.
- Coverage/overlap: complete and disjoint after `owise`. In the original
  supplied value signature, the true cases are precisely values injected from
  `Str`.
- Role/state: pure domain predicate; no cells or control.
- Decision: sound.

## `allStrings`

- Inventory: one `[function,total]` declaration and empty/cons rules.
- Coverage/overlap/descent: the free `ValSeq` constructors are covered
  disjointly; recursion strictly consumes the tail.
- Role/state: pure structural domain predicate; no cells or control.
- Decision: sound.

## `projectString` and cast/ceil simplifications

- Inventory: one `[function,total,symbol,no-evaluators]` declaration; one cast
  definedness rule; two guarded cast/projection orientations; one static
  identity; one idempotence rule.
- Domain: every equality that identifies a projection with its argument is
  guarded by `isStringValue`, or has a statically `Str` argument.
- Truth: for an original supplied-semantics value, `isStringValue(V)` means
  `V` is a `Str`; the partial sort cast is therefore defined and is exactly
  `V`. The `#Ceil` rule states this same membership condition. Static identity
  and idempotence follow.
- Overlap: on `str(CS)`, all applicable routes normalize to `str(CS)`. The
  orientations do not produce competing values. The `total` declaration leaves
  `projectString(non-string)` opaque; no rule equates such a term to a real
  source string.
- Role/state: result-bearing sort refinement used only by length; no cells or
  control.
- Decision: sound on the complete intended source domain. Synthetic
  `projectString(non-string)` terms extend the proof signature but are not
  source values and do not constrain real strings.

## `seqLenString`

- Inventory: one `[function,total,symbol,no-evaluators]` declaration and one
  constructor equation.
- Coverage: every original source `Str` is `str(CS)`, where the equation
  returns `isLen(CS)`. Synthetic proof-only `Str` terms may remain opaque under
  totality.
- Truth/overlap/descent: the equation is exactly the supplied
  `seqLen(str(CS)) => isLen(CS)` equation; there is no competing equation.
- Value influence: determines the loop branch and final string.
- Decision: sound for every intended string.

## `scanLongest`

- Inventory: one `[function,total]` declaration and empty/cons rules.
- Coverage/overlap/descent: empty and cons are disjoint and complete; recursion
  strictly consumes the tail.
- Truth: on strings, it replaces the accumulator exactly when the current
  length is strictly greater. Thus equality retains the earlier accumulator.
  By induction on the consumed prefix, the accumulator is the first element of
  maximum length in that prefix.
- Non-string totalization: if the current value or accumulator is not a string,
  the guarded branch retains the accumulator. Target claims require all
  elements and the initial accumulator to be strings.
- Role/state: pure postcondition summary; it never rewrites a source program
  term and touches no cells.
- Decision: sound.

## `longestValue`

- Inventory: one `[function,total]` declaration and empty, string-head, and
  non-string-head rules.
- Coverage/overlap: empty is disjoint from cons. `isStringValue(V)` and its
  Boolean negation partition cons heads, so the two guarded cons rules do not
  disagree.
- Truth: empty maps to `noneV`; a nonempty intended list seeds `scanLongest`
  with its first element. This is exactly the source contract. The non-string
  fallback is outside the source type domain.
- Role/state: pure final postcondition summary.
- Decision: sound.

## Guarded dynamic `seqLen` bridge

- Inventory: one `[simplification]` rule in module `VERIFICATION`.
- Class: operational bridge for a pure result-bearing operation.
- Complete match: `seqLen(V:Val)` in any pure term context, guarded by
  `isStringValue(V)`. It matches no configuration cell and changes no
  continuation, stack, binding, heap, exception, or exit state.
- Fixed behavior: for every actual source match, `V = str(CS)`. Fixed semantics
  yields `isLen(CS)`; the bridge yields
  `seqLenString(projectString(str(CS)))`, which normalizes to the same
  `isLen(CS)`.
- Overlap: on `str(CS)`, the fixed rule and bridge agree. The bridge's broader
  synthetic proof-signature cases do not correspond to source inputs.
- Connection evidence: the separately compiled `VERIFICATION-BASE` definition
  omits this bridge. Its two universal constructor claims close. The length
  claim is trivial because both sides independently normalize to `isLen(CS)`;
  triviality is evidence of definitional equality, not an oracle.
- Decision: sound and context-contained on the complete intended domain.

## Loop circularity

- Inventory: one claim, `SPEC.loop-invariant`.
- Complete match: the exact `#loop(list(REST), Name("string"), BODY)` term,
  current local scope, module scope, builtin scope, arbitrary following
  continuation, and framed unmentioned cells.
- Preconditions: all remaining elements, accumulator, and current loop
  variable are strings; the local location differs from module/builtin
  locations; the module does not shadow builtin `len`.
- State footprint: `result` changes from `ACC` to
  `scanLongest(REST,ACC)`; `string` is existentially updated to the last
  iterated value. `strings`, module bindings, heap, allocation counter, stack,
  return state, exception, exit status, and continuation are framed.
- Control: one fixed-semantics iteration binds the head, executes both actual
  `len` calls and the actual comparison/conditional assignment, then returns
  to the same loop head on the tail. The base case consumes `#iterDone`.
  There is no abrupt control in the loop body.
- Decision: sound circularity over arbitrary finite `REST`.

## Entry claims

- `empty-input`: exact initial state, exact submitted module, and exact call on
  `.ValSeq`; no additional precondition; result is `noneV`.
- `nonempty-input`: exact initial state/module/call on
  `vCons(FIRST,REST)`; precondition is precisely a nonempty finite list whose
  values are strings; result is the fully defined `longestValue`.
- Both claims execute function binding, lookup, argument binding, branching,
  indexing, iteration, calls, return, and frame pop under fixed semantics.
  Final scopes are existential because call/module execution materializes
  bindings; all other observable cells are fixed by the right-hand pattern.
- Decision: sound, result-constraining, and complete for arbitrary finite
  `List[str]`.

## Connection claims

- `string-length-connection`: under the bridge-free base module, both sides
  reduce independently to `isLen(CS)`.
- `string-projection-connection`: under the bridge-free base module, the
  defining static-string equation reduces the projection to `str(CS)`.
- Decision: sound supporting claims. They establish constructor-level
  equivalence for all original `Str` values; they are not treated as a proof
  of Python string semantics beyond the supplied IntSeq model.
