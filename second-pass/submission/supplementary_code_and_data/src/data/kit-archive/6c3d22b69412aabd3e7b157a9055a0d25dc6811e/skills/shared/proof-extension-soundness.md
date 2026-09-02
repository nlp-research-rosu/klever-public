# Proof-extension soundness contract

Use this contract whenever a proof adds a function, equation, claim, or rewrite
that contributes to closing a reachability claim. A successful kprove run
establishes closure under the supplied theory; validate that theory before
claiming a proof of the program.

## Classify every proof extension

| Class | Meaning | Required justification |
|---|---|---|
| Definitional summary | Names a mathematical value without replacing program execution | Truthful, guarded, terminating equations covering every use |
| Derived lemma | States a consequence of fixed semantics or established mathematics | A derivation valid over the lemma's complete guard |
| Operational bridge | Replaces or accelerates a term fixed semantics would execute | Equivalence to the exact execution, binding, control, and state transition |
| Trusted primitive | Represents a fixed operation intentionally outside the theorem | An explicit conditional trust boundary and independent evidence where available |

Classify by behavior, not by the symbol's name. A rule called a summary is an
operational bridge when it rewrites a program term before fixed semantics can
execute it. Program-defined code belongs to the program under verification; do
not reclassify it as an external primitive because proving it is difficult.

Before admitting an operational bridge, require a bridge-free universal
connection theorem over the bridge's complete match domain. The theorem must
not import the proposed bridge; it must establish the connection using fixed
semantics and independently justified theory. Finite tests do not satisfy this
precondition.

## Gate A — Real-program soundness

Gate A is mandatory. A failed obligation means the proof does not establish the
stated theorem about the program.

### A1. Program identity and body sensitivity

Let every relevant program-defined operation execute under fixed semantics, or
prove an auxiliary reachability claim from its exact invocation configuration,
binding, body, arguments, and environment to the stated summary. When practical,
mutate the body temporarily: a material body change must invalidate or change
the connection proof.

This pattern is not justified by an opaque result alone:

~~~k
rule <k> invoke(F, ARGS) => resultSummary(F, ARGS) ... </k>
~~~

If F denotes program-defined code, connect resultSummary to execution of that
code before using it in the caller's proof.

### A2. Operational-state preservation

For every operational bridge, enumerate the cells read, written, preserved, or
abstracted by the skipped execution. Preserve returned values, state changes,
resource changes, exceptions, output, and control effects exposed by the active
semantics. Prefer executing fixed semantics and summarizing the resulting value.

### A3. Binding, evaluation, and control fidelity

Preserve lookup, argument evaluation, evaluation order, control transfer, and
exceptional behavior. A textual operation name does not establish the selected
binding. If a bridge pins a binding, prove its environment and guard select that
binding.

#### Value fidelity for result-bearing abstractions

An abstraction is **result-bearing** when its value can affect a branch,
returned value, observable state, exception, or any summary used by the final
claim. First classify its origin. A fixed external primitive intentionally
outside the theorem may remain opaque when the proof is interpretation-
parametric or states every value-level conclusion conditionally on its named
contract. A program-derived abstraction has no such boundary: if an operational
bridge replaces fixed execution with a fresh or opaque symbol, require a
machine-checked connection theorem over the bridge's complete domain showing
that fixed semantics produces exactly that value. Exact syntax, bindings, and
context do not establish value equivalence.

This shape is circular rather than justificatory:

~~~k
rule <k> programExpression(X) => oracle(X) ... </k>
claim <k> program(X) => resultUsing(oracle(X)) </k>
~~~

Using the same fresh symbol in both the operational bridge and the postcondition
only makes the claim follow under an arbitrary interpretation of `oracle`; it
does not prove what the program expression computes. A program-defined
condition or property cannot become a trusted primitive by being opaque.
Execute it, define the summary truthfully and prove the connection, or reject
the proposed bridge and follow the Gate A repair transition. Finite tests can
expose a bad oracle but cannot replace the universal connection theorem.

For program-derived abstractions, use value-sensitivity witnesses independently
of context and postcondition mutations. Choose satisfiable ground cases with
distinct fixed-semantics values, compare fixed and bridge-enabled execution,
and attempt the opposite ground interpretation of the abstraction. Any admitted
wrong branch, result, or observable state is a Gate A failure.

#### Context containment for operational bridges

For every operational bridge, the bridge match domain must be a subset of its
justification domain. Compare complete configurations, not only the term being
summarized: include the active continuation, control stack, guards, bindings,
and every framed or omitted cell. A frame, wildcard, weaker guard, or omitted
cell broadens the bridge unless the supporting theorem is equally general or a
separate theorem proves that context irrelevant.

An exact auxiliary theorem over one continuation does not justify a rule over
an arbitrary continuation. Schematically:

~~~k
// Established only for this suffix:
claim <k> region(X) ~> finish(X) ~> #end => result(X) ... </k>

// Not derived: `...` admits suffixes the claim did not cover.
rule <k> region(X) => Return(result(X)) ... </k>
~~~

The second rule also introduces abrupt control that may discard or unwind the
framed computation. A bridge involving return, frame popping, exceptions, loop
control, cleanup, or another control effect must match the exact control context
or be justified by a theorem quantified over every context it accepts. Rule
priority can make a bad bridge preempt fixed semantics; it never supplies the
missing equivalence.

Use an operational-sensitivity mutation independently of A5: materially change
the displaced execution or an immediate continuation admitted by the bridge.
The connection proof must fail or its result must change when fixed execution
changes. This is separate from a postcondition mutation, which tests whether the
claim constrains its result but not whether a bridge preserves execution.

### A4. Logical consistency and rule validity

Require every equation to be true wherever its guard applies. Check equations
for the same symbol pairwise: guards must be disjoint or right-hand sides must
agree on their overlap. Check totality coverage, recursive descent, concrete and
simplification interactions, and totalization guards.

Do not justify a globally false rule only by calling its bad cases unreachable.
An off-path false rule blocks full validation until narrowed because later claims
or reuse can expose it.

### A5. Result constraint and non-vacuity

Exhibit a realizable state satisfying the precondition. Confirm that the final
claim constrains the relevant result or state and that required auxiliary claims
are exercised. Mutate the result or postcondition to a false alternative and
require the prover to reject it for a meaningful witness.

## Gate A repair transition

Gate A PASS continues to Gates B and C. Gate A failure is a repair signal, not
a terminal result. Every Gate A failure takes this back-edge unless an
enumerated, evidenced hard blocker prevents further repair. Within the same
agent invocation:

1. remove or disable every offending extension;
2. rerun without those extensions to recover the genuine residual; and
3. return to `proving-spec` to repair the construction, rebuild it, recover
   `#Top`, and reapply Gate A.

Only after repair attempts encounter an evidenced hard blocker may the workflow
produce terminal `Incomplete work`. Hard blockers are unavailable required tools
or inputs, an out-of-scope fixed-semantics language gap, repeated external
backend or resource failure, or inconsistent requirements. Record the evidence
and the repair attempts that exposed the blocker.

A difficult proof is not a hard blocker. A slower safe encoding is not a hard
blocker. Repair that requires redesign is not a hard blocker. `#Top` obtained
only through an unsound shortcut is not a hard blocker and is not a usable proof
state.

## Gate B — Intent adequacy

Gate B asks whether a sound theorem matches the intended property.

### B1. Input-domain alignment

Compare the formal precondition with the source contract, type information,
examples, and stated intent. Record every restriction rather than silently
strengthening the input contract.

### B2. Language-model adequacy

Identify material differences between fixed semantics and the intended execution
model, including numeric representation, exceptional behavior, text encoding,
collections, external state, concurrency, and implementation-defined behavior.

### B3. Summary-to-property adequacy

Separate a summary's execution characterization from the theorem that the
summary has the requested human-facing meaning. Label that bridge as formally
proved, conditionally trusted, or empirically supported.

### B4. Implementation-to-intent alignment

When the theorem faithfully describes the program but the program conflicts
with its specification, report an implementation/specification discrepancy. Do
not make the proof claim behavior the program does not have.

## Gate C — Trust and evidence auditability

### C1. Trust ledger

For every unproved component, record the exact symbol or rule, why it is outside
the theorem, whether it affects value, control, state, or termination assumptions,
which claims depend on it, and what evidence supports it.

### C2. Reproducible evidence

For every claimed differential, mutation, or concrete test, record an existing
artifact, exact command, input scope, oracle, and result. Finite testing supports
an assumption or adequacy bridge; it does not prove a universal equivalence.

### C3. Honest result language

Separate formally established facts, conclusions conditional on named
assumptions, empirically supported bridges, and excluded behavior.

## Proof-extension record

Record each extension during construction. Validation must rebuild this inventory
from the actual proof files rather than trusting the construction record.

| Field | Required content |
|---|---|
| Extension | Exact symbol, rule, or claim |
| Class | One of the four classes above |
| Semantic role | Whether it reasons about or replaces execution |
| Domain | Complete guard and assumptions |
| Matched context | Complete term, continuation, control stack, bindings, and framed cells accepted by the extension |
| Justification scope | Exact configurations established by the derivation, auxiliary theorem, or trust assumption |
| Context containment | Why every matched configuration lies within the justification scope |
| State footprint | Cells read, written, preserved, or abstracted |
| Value influence | Branches, results, state, exceptions, and postconditions affected by the extension's value |
| Value justification | Defining equations, connection theorem, or external contract that fixes each result-bearing value |
| Justification | Derivation, auxiliary theorem, or named trust assumption |
| Dependents | Claims whose closure relies on it |
| Control validation | Fixed-versus-extended comparison and operational-sensitivity evidence for control-affecting bridges |
| Value validation | Fixed-versus-extended witnesses and rejected opposite interpretations for result-bearing abstractions |
| Validation | Gate checks and reproducible evidence |

## Decide the report status

Record PASS or FAIL for every completed gate. Choose the headline status only
after the Gate A repair transition reaches PASS or an evidenced hard blocker:

| Result | Status |
|---|---|
| Gate A remains blocked after evidenced repair attempts | Incomplete work; do not issue a successful proof report |
| Gate A passes and Gate B fails | SOUND-BUT-LIMITED |
| Gates A and B pass and Gate C fails | FORMALLY-SOUND-UNVALIDATED |
| Gates A, B, and C pass | VALIDATED |

Always report later-gate failures even when an earlier gate determines the
headline status.

## Red flags — stop before reporting success

| Rationalization | Required response |
|---|---|
| “The shortcut is only an optimization.” | Classify it by the execution it replaces and prove full equivalence. |
| “The false case is unreachable.” | Narrow the guard so the rule is true wherever it applies. |
| “Differential tests prove the abstraction.” | Report finite evidence; provide a theorem for universal equivalence. |
| “The source helper is trusted.” | Execute program-defined code or prove an exact auxiliary execution claim. |
| “The return value is right.” | Compare binding, control, exceptions, and every observable state cell. |
| “The same symbol appears in execution and the spec.” | That is circular unless fixed execution is independently connected to the symbol's value. |
