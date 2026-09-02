# Used-construct and proof-extension review

## Scope

The exhaustive machine-generated inventory is `05_rule_inventory.md` (946
declarations: 705 rules, 233 syntax declarations, five contexts, two claims,
and one configuration). The candidate's entire `reference-semantics/` tree is
identical to the trusted supplied baseline. The table below isolates every
construct that can occur on the submitted program's proof path; all other
inventoried fixed-semantics declarations are unreachable by sort/constructor
dispatch from this AST and are marked as unused in the exhaustive inventory.

No `[simplification]` rule and no `[functional]` declaration occurs in the
supplied or proof-local sources. The fixed baseline has 22 `no-evaluators`
opaque symbols:

- Float-related: `intFloatDiv`, `divII`, `floatMod`, `floatLt`, `absF`,
  `subF`, `divF`, `addF`, `mulF`, `powF`, `gtF`, `eqF`, `decStrToF`,
  `divFloatIntV`, `intToF`, `truncF`, `roundF`, `roundFN`, and `sqrtF`.
- Sorting: `sortVS` and `sortKeyVS`.
- Hashing: `md5hexCodes`.

None appears in `solution.mpy`, either candidate claim, a proof-local summary,
or a residual on a successful proof path. They cannot influence control,
state, or the result of the audited claims.

## Submitted AST to fixed semantics

| Submitted construct | Declaration/evaluation rules | Audit decision |
|---|---|---|
| `Module` | `semantics/syntax.k:61`; initial `#loadAll` configuration and rules at `semantics/core.k:49,124-127` | Faithful module sequencing. The candidate's **proof claim does not exercise it**. |
| `FuncDef("encrypt", Params("s"), ...)` | `semantics/syntax.k:53`; closure installation at `semantics/functions.k:14-16` | Faithful fixed rule. The candidate's proof bypasses it by preinstalling `encryptClosure`. |
| `Assign(Name(...), Str(...))` | strict RHS at `semantics/syntax.k:41`; string literal at `semantics/str.k:13-17`; assignment at `semantics/controls.k:9-11` | Deterministic left-to-right behavior and exact local-map update. |
| `Name` | grammar at `semantics/syntax.k:12`; lookup/parent walk at `semantics/core.k:130-154`; `builtinsScope` at `semantics/core.k:157-181` | Binding-sensitive. This sensitivity is precisely what the candidate loop bridge fails to preserve over its declared match domain. |
| `For` / string iteration | strict iterable at `semantics/syntax.k:45`; loop at `semantics/controls.k:65,69-74`; string iterator at `semantics/str.k:8-10`; target binding at `semantics/tuple.k:31-35` | Fixed rules evaluate the iterable once, bind each one-character string, execute the body, and retain the final target binding. |
| `AugAssign` | strict RHS at `semantics/syntax.k:44`; update at `semantics/controls.k:20-23` | Reads the current local and applies the relevant `applyBin`; exact for the string accumulator. |
| `Call` | syntax at `semantics/syntax.k:28`; callee/argument route at `semantics/call.k:19-32`; left-to-right argument fold at `semantics/core.k:185-191` | Preserves callee binding and argument order. |
| User-function invocation | closure dispatch/frame push at `semantics/call.k:69-74`; parameter binding at `semantics/functions.k:62-75` | Exact scope-1 creation, `s` binding, caller continuation, and stack frame. |
| `ord` / `chr` | builtin bindings at `semantics/core.k:165-166`; equations at `semantics/builtins.k:142-145` | `ord` consumes the one-code string yielded by the loop. `encryptCode` is always 97..122, satisfying the fixed `chr` ASCII guard. |
| Integer `-`, `+`, `%` | strict `BinOp` dispatch at `semantics/syntax.k:15` and `semantics/operators.k:12`; cases and `pyMod` at `semantics/int.k:9,13,15,19-20` | Implements `((C-97+4) mod 26)+97` with Python-style positive-modulus behavior. |
| String `+` | `semantics/str.k:20-24` | Structural concatenation with recursive descent on the left sequence. |
| `Return` | strict return at `semantics/syntax.k:50`; return/pop at `semantics/functions.k:77-90` | Produces the accumulator, restores env, drops scope 1, and resumes the saved continuation. |

The candidate macros at `verification.k:27-56` duplicate the translated
function body and closure shape, and their expression nesting agrees with
`solution.mpy`. They do not, however, import or load the submitted `Module`
artifact. The only candidate occurrence of the filename is the translator
regeneration command in `prove.sh:4`; the proof commands consume `spec.k` and
`verification.k`.

## Proof-local declarations, rule by rule

| Source | Classification | Coverage/overlap/descent | Result influence and decision |
|---|---|---|---|
| `verification.k:8-9`, `encryptCode` | Definitional mathematical summary | One unguarded equation covers every `Int`; denominator is fixed positive 26. | Fixes every output character to the same arithmetic formula as submitted Python. Sound as mathematics and contains no oracle. |
| `verification.k:11,13`, `encryptCodes` | Definitional wrapper | One equation covers every `IntSeq`. | Initializes an empty accumulator; sound. |
| `verification.k:11,14-18`, `encryptAcc` | Recursive definitional summary | `.IntSeq` and `iCons` cases are disjoint and exhaustive; recursive call strictly shortens the second sequence. | Determines the complete output sequence; sound. |
| `verification.k:22-25`, `lastChar` | Recursive definitional summary | `.IntSeq` and `iCons` cases are disjoint and exhaustive; recursive call strictly shortens the first sequence. | Determines the post-loop `char` binding, including the empty case; sound. |
| `verification.k:27-44`, `encryptLoopBody` | Source macro | Single expansion; no overlap. | Exact duplicate of the submitted loop body; sound syntax alias. |
| `verification.k:46-52`, `encryptFunctionBody` | Source macro | Single expansion; no overlap. | Exact duplicate of the function statement list; sound syntax alias. |
| `verification.k:54-56`, `encryptClosure` | Source macro | Single expansion; no overlap. | Names the duplicated closure. It is not a proof that `solution.mpy` was loaded. |
| `verification.k:66-88`, loop summary | Operational bridge, priority 40 | Its pattern admits arbitrary continuation and arbitrary other scope entries; it constrains only env 1, the exact local map at location 1, and an empty heap. | **Unsound on its declared match domain.** It ignores name bindings in parent/module/builtins scopes even though the displaced body looks up both `ord` and `chr`. |

## False-conclusion witness for the operational bridge

The ground witness in `bridge-witness.k` uses the intended lowercase input
`"a"` (code 97), the exact required location-1 locals, an empty heap, and a
well-formed module/builtins chain. Module scope 0 shadows `chr` with
`builtinV("ord")`.

Under bridge-free `VERIFICATION`, fixed semantics honors that binding. It
computes integer 101, dispatches the apparent `chr` call to `ord`, and reaches
the residual:

```text
applyBuiltin("ord", 101, .Vals)
```

The claimed result `"e"` is therefore not obtained; `kprove` exits 1 with
`WarnStuckClaimState`. Under `VERIFICATION-WITH-LOOP`, the priority-40 bridge
matches the same state, skips lookup/call/body execution, fabricates result
`"e"`, and proves the identical claim as `#Top` with exit 0. Exact commands and
outputs are in `04b_bridge_witness.log`.

The reviewer-authored universal connection claim matching the bridge's full
ellipsis-bearing domain also builds but fails under bridge-free semantics
(`04_bridge_check.log`). Its residual shows branches where parent scope 0 or a
`chr` binding is absent. Thus the candidate's narrower `LOOP-SPEC` theorem does
not justify the broader installed bridge.

This is not merely missing evidence: the ground pair is a concrete false
conclusion enabled by the proof rule for an intended-domain input. The rule
must have constrained the parent binding environment to the one proved in
`LOOP-SPEC` (and its continuation scope justified), or the function proof must
have composed the exact auxiliary claim without installing this global rule.
