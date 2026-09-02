# Reviewer rule inventory

This inventory is reconstructed from the immutable candidate sources copied to
`/tmp/audit-work/candidate-src`. “Sound” below is relative to the explicitly
represented `PyVal` algebra and the exact submitted program. It does not by
itself establish an encoding theorem from unrestricted CPython `Any` values.

## `semantic.k`: local syntax and configuration

- Lines 8-9: `Module(Module(Stmts))` and the juxtaposed `Stmts` list.
- Lines 10-12: `Stmt` alternatives `ImportFrom`, `FuncDef`, and `Return`.
- Lines 14-15: `Params` and comma-separated `Strings`.
- Lines 17-23: `Expr` alternatives `Name`, `Int`, `Bool`, `Str`, `ListExpr`,
  `Call`, and `ListComp`.
- Lines 24-26: comma-separated `Exprs`, `CompFor`, and juxtaposed `CompFors`.
- Lines 30-38: `PyVal` alternatives `VInt`, `VBool`, `VString`, `VFloat`
  (string payload), `VList`, `VDict`, `VNone`, and `VOpaque`, plus `PyVals`.
- Lines 45-57: runtime syntax `RuntimeFunction`, linked `Functions`, linked
  `Env`, `Result`, and K items `bootstrap`, `load`, `invoke`, `exec`, `finish`.
- Lines 59-66: configuration cells `<k>`, `<program>`, `<functions>`, `<env>`,
  and `<return>`. All five are read or changed by at least one used rule.

No local syntax is declared `[functional]` or opaque. There are no explicit
`priority` attributes and no `[simplification]` rules. The two `[owise]`
equations below have generated lower priority.

## `semantic.k`: operational and equational rules

| ID | Lines | Rule / domain | Disposition |
|---|---:|---|---|
| S1 | 68-69 | `bootstrap` reads `Module(SS)` and schedules `load(SS)` | Sound for the submitted module; preserves the continuation. |
| S2 | 71 | `load(.Stmts)` consumes loading | Sound list base case. |
| S3 | 72 | `load(ImportFrom(_,_) SS)` skips the import | Sound for this typing-only import as used: translated annotations are absent and `List`/`Any` are never read. Import exceptions, bindings, and side effects are outside the model. |
| S4 | 73-74 | load a one-parameter function and prepend its binding | Sound for the single submitted definition. Multiple parameters/closures are deliberately unsupported. |
| S5 | 76-78 | invoke the head binding, reset the local environment, bind one argument | Sound for the one-function module and exact call. Missing/non-head bindings remain visibly stuck. |
| S6 | 80-81 | execute the singleton `Return(E)` via `eval(E, ENV)` | Sound for the exact one-statement body; general return control and later statements are unsupported. |
| S7 | 83-84 | `finish(V)` consumes computation and records `result(V)` | Sound in this call-stack-free submitted program. |
| E1 | 87 | `eval(Int(I),_) = VInt(I)` | Truthful; unused by the source body. |
| E2 | 88 | `eval(Bool(B),_) = VBool(B)` | Truthful; unused by the source body. |
| E3 | 89 | `eval(Str(S),_) = VString(S)` | Truthful; unused by the source body. |
| E4 | 90 | lookup at the head `bind(X,V,_)` | Truthful. |
| E5 | 91-92 | skip a different name while looking up | Truthful and descending on `Env`; empty misses remain stuck. |
| E6 | 93 | empty source list evaluates to empty runtime list | Truthful; nonempty source literals are unmodeled and unused. |
| E7 | 94-95 | exact built-in-looking `isinstance(E,int)` maps through `pythonIsInteger` | Correct for the submitted unshadowed builtin names, conditional on the `PyVal`/CPython type bridge below. It is result-bearing. |
| E8 | 96-97 | exact one-generator/one-filter list comprehension invokes `comprehend` | Matches the submitted AST exactly. Other comprehension forms remain stuck. |
| T1 | 100 | `pythonIsInteger(VInt(_)) = true` | Truthful if `VInt` denotes integer instances. |
| T2 | 101 | `pythonIsInteger(VBool(_)) = true` | Truthful for CPython: `bool` is an `int` subclass. |
| T3 | 102 | all other `PyVal` constructors map to false, `[owise]` | Disjoint from T1/T2 by `owise` and completes `[total]` over `PyVal`. Truth is conditional on the constructor interpretation; the artifacts give no universal encoding for custom `int` subclasses. |
| C1 | 106 | comprehend the empty list to an empty list | Truthful base case. |
| C2 | 107-110 | evaluate condition/projection for a head and recurse on the tail | Truthful for the exact pure `Name("value")` projection and boolean `isinstance` condition. The modeled expression subset has no observable side effect with which to distinguish evaluation schedules. |
| K1 | 113 | a true condition prepends the projected value | Truthful. |
| K2 | 114 | a false condition discards the projection | Truthful. |
| P1 | 119 | prepend to a runtime list | Truthful and constructor-preserving. |

`eval`, `comprehend`, `keepIf`, and `prepend` are `[function]` but not
`[total]`; unsupported terms therefore remain stuck. `pythonIsInteger` is the
only `[function,total]` declaration in this file; T1-T3 are constructor-complete
and non-overlapping under `owise`.

## `verification.k`: syntax, functions, equations, and priorities

- Lines 9-17: nullary `[function]` `solutionModule()`, with one complete
  equation expanding to the exact translated module.
- Lines 19-23: nullary `[function]` `filterExpression()`, with one complete
  equation for the submitted list comprehension.
- Lines 25-27: nullary `[function]` `filterCondition()`, with one complete
  equation for `isinstance(value, int)`.
- Lines 31-48: `[function,total]` `onlyIntegerInstances(PyVals)` and nine
  equations: empty; retain `VInt`; retain `VBool`; drop each of `VString`,
  `VFloat`, `VList`, `VDict`, `VNone`, and `VOpaque`. Constructor cases are
  disjoint, exhaustive over `PyVals`, and recurse on a strict tail.
- Lines 50-56: `[function,total]`
  `containsOnlyIntegerInstances(PyVals)` and four equations: empty is true;
  `VInt` and `VBool` recurse; the `[owise]` cons case is false. The `owise`
  case has lower priority, so overlaps with the two retain cases do not change
  their results. Coverage is complete over `PyVals`.

There are no local opaque symbols, `[functional]` declarations, operational
bridges, ordinary state-changing rules, explicit priority attributes, auxiliary
claims, or simplification rules in `verification.k`. All local rules are
definitional equations. They are truthful inside the modeled algebra, but
`onlyIntegerInstances` is not connected by a universal submitted reachability
claim to execution of the program.

## `spec.k`: all submitted claims

1. Lines 10-14: empty `comprehend` base.
2. Lines 16-22: one `VInt` head step with arbitrary tail left as a residual
   `comprehend`.
3. Lines 24-30: one `VBool` head step with arbitrary tail left residual.
4. Lines 32-37: one `VString` head step.
5. Lines 39-44: one `VFloat` head step.
6. Lines 46-51: one nested-`VList` head step.
7. Lines 53-58: one `VDict` head step.
8. Lines 60-65: one `VNone` head step.
9. Lines 67-72: one `VOpaque` head step.
10. Lines 76-82: fixed three-element heterogeneous evaluation/model equality.
11. Lines 86-102: full module execution for prompt example one.
12. Lines 104-124: full module execution for prompt example two.
13. Lines 127-130: fixed empty expression evaluation.
14. Lines 132-138: fixed five-element bool/integer boundary evaluation.
15. Lines 142-151: fixed-length nine-element symbolic-payload evaluation.
16. Lines 155-161: all-integer property for one fixed seven-element sequence.
17. Lines 163-168: exact stable-filter result for that same fixed sequence.

There are no logical `requires` or `ensures` clauses, no circularity/invariant
claim, and no claim whose input is `VList(VS:PyVals)` and whose terminal return
is `VList(onlyIntegerInstances(VS))`. Claims 1-9 are one-step characterizations,
not a reachability induction to a terminal result. Claims 10 and 13-17 have
fixed list lengths. Claims 11-12 are the only full-program entry claims and
both have ground inputs.

## Trust and gap classification

- No locally false K equation was identified within the uninterpreted
  constructor algebra, so this review does not label any rule “unsound.”
- The result-bearing bridge from CPython objects/types to `PyVal` constructors
  is unstated and unproved. A concrete adequacy witness is an instance of a
  user-defined subclass of `int`: CPython retains the original object; the K
  algebra has no constructor that both records the subtype/object identity and
  is classified true. Encoding it as `VOpaque` makes T3 discard it; encoding it
  as `VInt(I)` erases the subtype/object distinction.
- Even restricted to the finite `PyVal` algebra, the submitted claims never
  state the unrestricted terminal-result theorem. The reviewer’s
  `universal-entry-spec.k` is that missing claim and gets stuck on symbolic
  `comprehend(VList(VS), ...)`.
