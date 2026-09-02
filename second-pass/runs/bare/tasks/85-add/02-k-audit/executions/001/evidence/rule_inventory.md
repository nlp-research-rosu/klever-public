# Reviewer rule inventory

Source hashes are in `01-integrity-hashes-and-cmp.log`; source text with line
numbers is in `02-trusted-contract-and-candidate-sources.log`.  IDs below are
reviewer-assigned.

## Modules, imports, configuration, and syntax

- `MPY-SYNTAX` imports `INT-SYNTAX`, `BOOL-SYNTAX`, and `STRING-SYNTAX`.
- `MPY` imports `MPY-SYNTAX`, `INT`, `BOOL`, `STRING`, `MAP`, and `LIST`.
- `VERIFICATION` imports `MPY`; `SPEC` imports `VERIFICATION`.
- The sole configuration is `<mpy>` with `<k> $PGM:Module ~> start </k>`,
  `<input> $INPUT:PyVal </input>`, and initially empty `<functions>`, `<env>`,
  and `<callStack>` cells.

Every local syntax declaration:

| ID | Source | Declaration and attributes |
|---|---|---|
| S01 | semantic.k:6 | `Module ::= Module(Stmts)` `[symbol]` |
| S02 | semantic.k:7 | `Stmts ::= List{Stmt,""}` |
| S03 | semantic.k:8-9 | `Stmt ::= FuncDef(String,Params,Stmts) \| Return(Expr)`; both `[symbol]` |
| S04 | semantic.k:10 | `Params ::= Params(String)` `[symbol]` |
| S05 | semantic.k:12-18 | `Expr ::= Int(Int) \| Name(String) \| BinOp(String,Expr,Expr) \| Compare(Expr,CmpOp) \| Subscript(Expr,Index) \| Call(Expr,Expr) \| IfExp(Expr,Expr,Expr)`; all `[symbol]` |
| S06 | semantic.k:19 | `CmpOp ::= CmpOp(String,Expr)` `[symbol]` |
| S07 | semantic.k:20-21 | `Index ::= Expr \| Slice(Bound,Bound,Bound)`; `Slice` `[symbol]` |
| S08 | semantic.k:22 | `Bound ::= Expr \| NoBound`; `NoBound` `[symbol]` |
| S09 | semantic.k:26-27 | `ISeq ::= nil \| cons(Int,ISeq)`; both `[symbol]` |
| S10 | semantic.k:28-30 | `PyVal ::= pyInt(Int) \| pyBool(Bool) \| pyList(ISeq)`; all `[symbol]` |
| S11 | semantic.k:41 | `FuncInfo ::= function(String,Expr)` `[symbol]` |
| S12 | semantic.k:43-57 | control `KItem`s: `start`, `done`, `eval`, `select`, `binRight`, `binApply`, `cmpRight`, `cmpApply`, `isShortList`, `keepIfEven`, `indexAt`, `sliceFrom`, `builtInLen`, `userCall`, `restoreCaller` |
| S13 | semantic.k:150 | `size(ISeq):Int` `[function,total]` |
| S14 | semantic.k:154 | `at(ISeq,Int):Int` `[function]` |
| S15 | semantic.k:159 | `drop(ISeq,Int):ISeq` `[function]` |
| S16 | semantic.k:164 | `evenPart(Int):Int` `[function]` |
| S17 | verification.k:8 | `oddIndexEvenSum(ISeq):Int` `[function]` |
| S18 | verification.k:15 | `solutionProgram:Module` `[macro]` |

There are no `[functional]` declarations, simplification rules, fresh values,
or opaque result functions.  The `[symbol]` declarations are AST/value
constructors rather than unconstrained result oracles.  The compiler warns
that zero-argument `symbol` lacks an explicit `klabel`, but both clean builds
accept it and it does not change rule truth.

## Exhaustive rule decisions

| ID | Source | Rule | Classification and decision |
|---|---|---|---|
| R01 | semantic.k:71-72 | load `FuncDef` into `<functions>` | Ordinary semantic rule; correct for the submitted one-function module and preserves all other cells. |
| R02 | semantic.k:74-75 | after loading, invoke designated `add` on `<input>` | Ordinary entry rule; correct for the trusted problem entry point. |
| R03 | semantic.k:77 | remove `done` after a `PyVal` | Ordinary control rule; value and suffix are preserved. |
| R04 | semantic.k:79 | evaluate integer literal | Ordinary semantic rule; truthful. |
| R05 | semantic.k:80-81 | look up a name in `<env>` | Ordinary semantic rule; binding is selected by the map lookup. |
| R06 | semantic.k:87-89 | specialize `len(ARG) < 2` to `eval(ARG) ~> isShortList` `[priority(40)]` | Operational bridge. For a `pyList` it is extensionally the generic `len`/compare path; for other `PyVal`s both paths stop. It evaluates `ARG` once and preserves the arbitrary suffix and every state cell. Accepted on the actual program domain. |
| R07 | semantic.k:90 | `nil` is short | Bridge equation; `len=0`, truthful. |
| R08 | semantic.k:91 | singleton is short | Bridge equation; `len=1`, truthful. |
| R09 | semantic.k:92 | two-or-more list is not short | Bridge equation; truthful and disjoint from R07/R08. |
| R10 | semantic.k:94-98 | specialize `ITEM if ITEM % 2 == 0 else 0` to one evaluation plus `keepIfEven` `[priority(40)]` | Result-bearing operational bridge. The modeled expression language has no mutation, I/O, allocation, or nondeterminism, so repeated evaluation of the syntactically identical `ITEM` cannot change its value or state. The suffix is preserved. `evenPart` is fixed by R38/R39. Accepted for the submitted program; concrete fixed-generic comparisons cover even, odd, negative, recursive, and live-continuation witnesses. |
| R11 | semantic.k:99 | `pyInt(I) ~> keepIfEven` becomes `pyInt(evenPart(I))` | Definitional bridge tied to exhaustive, disjoint R38/R39; no fresh value. |
| R12 | semantic.k:101-102 | evaluate conditional guard first | Ordinary sequencing rule; matches Python conditional-expression order. |
| R13 | semantic.k:103 | select true branch | Ordinary semantic rule; only selected branch is evaluated. |
| R14 | semantic.k:104 | select false branch | Ordinary semantic rule; disjoint from R13. |
| R15 | semantic.k:106-107 | evaluate binary left operand first | Ordinary sequencing rule; correct. |
| R16 | semantic.k:108-109 | then evaluate binary right operand | Ordinary sequencing rule; preserves left value in continuation. |
| R17 | semantic.k:110 | integer `+` | Trusted K arbitrary-integer primitive; matches Python integers. |
| R18 | semantic.k:111 | integer `%` | Trusted K integer primitive. Actual divisor is positive `2`; zero/noninteger exceptional cases are not on the submitted path. |
| R19 | semantic.k:113-114 | evaluate comparison left first | Ordinary sequencing rule; correct. |
| R20 | semantic.k:115-116 | then evaluate comparison right | Ordinary sequencing rule; correct. |
| R21 | semantic.k:117 | integer `<` | Trusted K integer primitive; truthful. |
| R22 | semantic.k:118 | integer `==` | Trusted K integer primitive; truthful. |
| R23 | semantic.k:120-121 | evaluate indexed subscript base | Ordinary sequencing rule; actual index expression is literal `1`. |
| R24 | semantic.k:122-123 | list index via `at` | Ordinary semantic rule. `at` is deliberately partial for invalid/negative positions; actual branch establishes length at least two and index is `1`. No false result is fabricated outside coverage. |
| R25 | semantic.k:124-125 | evaluate slice base for `[I:]` | Ordinary sequencing rule; actual `I` is literal `2`, other bounds are absent. |
| R26 | semantic.k:126-127 | list slice via `drop` | Ordinary semantic rule. `drop` is partial past the end, but the actual branch establishes at least two elements and uses `2`. |
| R27 | semantic.k:129-130 | evaluate `len` argument | Ordinary built-in sequencing rule. |
| R28 | semantic.k:131-132 | list length via `size` | Definitional primitive; R32/R33 fix the value. |
| R29 | semantic.k:134-136 | textual non-`len` name call becomes `userCall` | Ordinary call-dispatch rule. It is broader than full Python because it does not model local shadowing/first-class functions. On the submitted flow the only such name is global `add`, while the sole local binding is `lst`; therefore no false intended-domain witness exists. This is an adequacy limitation, not an unsound conclusion about the submitted program. |
| R30 | semantic.k:140-144 | enter user function, bind parameter, save caller env | Ordinary call rule; argument is already a `PyVal`, function map selects the exact body, caller environment is saved, and the live K suffix remains after `restoreCaller`. |
| R31 | semantic.k:146-148 | restore caller environment and stack | Ordinary return rule; result and arbitrary suffix are preserved, and the exact saved environment is restored. |
| R32 | semantic.k:151 | `size(nil)=0` | Function equation; truthful. |
| R33 | semantic.k:152 | `size(cons)=1+size(rest)` | Function equation; truthful, structurally descending, disjoint from R32. Together R32/R33 justify `[total]` over `ISeq`. |
| R34 | semantic.k:155 | `at(cons(head,_),0)=head` | Partial-function equation; truthful. |
| R35 | semantic.k:156-157 | positive index recurses with index minus one | Partial-function equation; guard is disjoint from R34 and recursion descends on both list and positive index. |
| R36 | semantic.k:160 | `drop(values,0)=values` | Partial-function equation; truthful. |
| R37 | semantic.k:161-162 | positive drop recurses with index minus one | Partial-function equation; guard is disjoint from R36 and recursion descends. |
| R38 | semantic.k:165-167 | even `I` gives `evenPart(I)=I` `[concrete]` | Definitional equation; guard is mathematically truthful. `[concrete]` restricts application, not truth. |
| R39 | semantic.k:168-170 | non-even `I` gives `evenPart(I)=0` `[concrete]` | Definitional equation; guard is the complement of R38. The pair covers every ground integer and has no overlap. |
| V01 | verification.k:9 | `oddIndexEvenSum(nil)=0` | Mathematical summary equation; truthful. |
| V02 | verification.k:10 | singleton summary is `0` | Mathematical summary equation; truthful and disjoint from V01/V03. |
| V03 | verification.k:11-12 | two-or-more summary is `evenPart(second)+summary(rest)` | Mathematical summary equation; exactly partitions odd indices by dropping two; structurally descending. |
| V04 | verification.k:16-33 | expand `solutionProgram` to a fixed `Module` AST | Compile-time macro, not an execution bypass. Fresh `kast` comparison proves exact expanded KORE identity with regenerated `solution.mpy`. |

No ordinary proof-local operational rules occur in `verification.k`; V01-V03
are definitional equations and V04 is a macro.  There are exactly two priority
rules (R06 and R10), exactly two `[concrete]` equations (R38 and R39), one
`[total]` declaration (S13), and zero simplification rules.

## Claims

- C01 (`spec.k:9-28`) universally summarizes a call to the exact stored `add`
  body.  Its suffix, input, caller environment, and caller stack are arbitrary
  but preserved; the function map is the exact singleton map used by the
  program.  This is the recursive induction/circularity claim.
- C02 (`spec.k:31-50`) starts with the exact `solutionProgram ~> start`,
  list-valued input, and empty maps/stack.  It requires the final K cell to be
  exactly `pyInt(oddIndexEvenSum(VALUES))` and records the exact loaded body.

## Construct coverage for `solution.mpy`

`Module`, `FuncDef`, `Params`, and `Return` use R01-R03; integer and name
expressions use R04-R05; the outer `IfExp` uses R06-R09 and R12-R14; the inner
parity `IfExp` uses R10-R11 plus R38-R39; outer addition uses R15-R17;
subscript/index and slice use R23-R26 plus R34-R37; recursive call/return uses
R29-R31; and list length is covered by R06-R09 (with the generic R27-R28 and
R32-R33 independently available).  The `%`, `==`, and `<` syntax used in the
submitted AST is either handled by the priority specialization or by its
generic R18-R22 baseline.  Every actually used constructor therefore has a
declaration and a sound reachable rule path.
