# Exhaustive local K inventory

Line numbers refer to the immutable candidate files.

## `semantic.k`: syntax and configuration

| ID | Lines | Declaration | Audit disposition |
|---|---:|---|---|
| S1 | 8 | `Ids ::= List{String, ","}` | Parameter-name sequence; used by the two names in `Params`. |
| S2 | 9 | `Params(String-list)` (`symbol`) | Exact translated parameter constructor. |
| S3 | 11 | `Exprs ::= List{Expr, ","}` | Call-argument sequence; one argument is used by `len`. |
| S4 | 12 | `CmpOp(String, Expr)` (`symbol`) | Exact translated comparison-pair constructor. |
| S5 | 13 | `CmpOps ::= List{CmpOp, ","}` | Comparison sequence; submitted program uses one pair. |
| S6–S11 | 15–20 | `Int`, `Str`, `Name`, `BinOp`, `Compare`, `Call` expression constructors (`symbol`) | These are exactly all expression constructors in `solution.mpy`; none computes merely by parsing. |
| S12 | 22 | `Stmts ::= List{Stmt, ""}` | Ordered statement sequencing, including `.Stmts`. |
| S13–S18 | 23–28 | `Module`, `FuncDef`, `Assign`, `If`, `For`, `Return` statement constructors (`symbol`) | Exactly all statement constructors in `solution.mpy`. |
| S19–S20 | 30–31 | `PyList ::= Nil \| Cons(Int, PyList)` (`symbol`) | Finite integer-list representation used for both inputs. |
| S21–S24 | 32 | `Val ::= Int \| String \| Bool \| PyList` | Runtime value injections needed by the submitted program. |
| S25–S26 | 33 | `Result ::= noResult \| Val` (`noResult` is `symbol`) | Explicit unset/returned-result state. |
| K1–K13 | 43–55 | `init`, `exec`, `eval`, `write`, `binRight`, `applyBin`, `cmpRight`, `applyCmp`, `doLen`, `branch`, `startFor`, `loop`, `finish` (`symbol`) | Internal control terms. Each is consumed by rules R3–R29 below; none is declared opaque. |
| F1 | 57 | `length(PyList):Int` (`function,total`) | Structural finite-list length; equations R1–R2 are disjoint, exhaustive, and decreasing. |
| CFG | 61–66 | `<exchange><k>…</k><env>.Map</env><result>noResult</result></exchange>` | Minimal state: computation, local environment, and return result. |

There are no candidate-local `functional` declarations or opaque symbols. The
many constructor `symbol` attributes give stable KORE identities; they do not
assert equations or opacity.

## `semantic.k`: every local rule

| ID | Lines | Rule | Class and soundness finding |
|---|---:|---|---|
| R1 | 58 | `length(Nil) => 0` | True structural equation. |
| R2 | 59 | `length(Cons(_,REST)) => 1 +Int length(REST)` | True, terminating structural equation. |
| R3 | 68–75 | Load exact one-function `exchange` module, bind `lst1/lst2`, seed `even/value`, execute `BODY` | Ordinary entry semantics. For the fixed submitted body, `even` is immediately overwritten and `value` is written before each loop-body read; the extra seeds cannot affect the returned value. It intentionally does not model arbitrary Python modules or reflection. |
| R4 | 77 | `exec(.Stmts) => .K` | Correct end of a statement sequence. |
| R5 | 78–79 | Assignment evaluates RHS, then `write`, then rest | Correct order for the used `Name` target. |
| R6 | 80–81 | `write(X)` updates environment binding | Correct local assignment state change. |
| R7 | 83–84 | `If` evaluates guard, then branches, then executes rest | Correct control order. |
| R8 | 85 | `true ~> branch(THEN,_) => exec(THEN)` | Correct true branch. |
| R9 | 86 | `false ~> branch(_,ELSE) => exec(ELSE)` | Correct false branch. |
| R10 | 91–99 | Priority-40 parity-counting idiom bridge | Operational bridge. `evenBit` is exhaustive and the bridge-free full-domain connection claim closes (`05_bridge_full.log`); bridge-enabled and bridge-free observable-continuation executions are identical (`05_bridge_context.log`). Sound, not an oracle. |
| R11 | 101–102 | `For` evaluates iterable, then `startFor`, then rest | Correct iterable-before-loop order. |
| R12 | 103–104 | A `PyList` and `startFor` become `loop` | Correct bridge into iteration. |
| R13 | 105 | `loop(_,Nil,_) => .K` | Correct zero-remaining-iteration case. |
| R14 | 106–107 | `Cons(I,REST)` writes target, executes body, recurs | Correct sequential list iteration and loop-variable update. |
| R15 | 109–110 | `Return(E)` evaluates E then `finish`, discarding later source statements | Correct return control effect. |
| R16 | 111–112 | A value at `finish` clears the continuation and sets result | Correct single-function return; environment is preserved and no other observable cell exists. |
| R17 | 114 | `eval(Int(I)) => I` | Correct literal. |
| R18 | 115 | `eval(Str(S)) => S` | Correct literal. |
| R19 | 116–117 | `eval(Name(X))` looks up `X` | Correct binding lookup for used names. |
| R20 | 119–120 | `BinOp` begins with left operand | Correct left-to-right order. |
| R21 | 121–122 | After left value, evaluate right, then apply | Correct left-to-right order. |
| R22 | 123–124 | Integer `+` | Trusted K unbounded-integer primitive; agrees with Python integers here. |
| R23 | 125–126 | Integer `%` | Used only with divisor 2. Zero/nonzero parity agrees with Python even for negative integers. |
| R24 | 128–129 | Comparison begins with left operand | Correct left-to-right order. |
| R25 | 130–131 | After left value, evaluate right, then apply | Correct left-to-right order. |
| R26 | 132–133 | Integer `==` | Correct used comparison. |
| R27 | 134–135 | Integer `>=` | Correct used comparison. |
| R28 | 137–138 | `Call(Name("len"),ARG)` evaluates ARG then `doLen` | Correct for the unshadowed builtin binding in the fixed program. |
| R29 | 139 | A list at `doLen` becomes `length(L)` | Correct used `len` operation. |

R10 is the only priority rule. There are no candidate-local simplification
rules in `semantic.k`.

## `verification.k`: macros, functions, and equations

| ID | Lines | Declaration/rule | Class and soundness finding |
|---|---:|---|---|
| M1 | 6–10 | `countBody` macro and expansion | Exact parity-counting `If` body from both real loops. |
| M2 | 12–22 | `solutionProgram` macro and expansion | Exact full submitted constructor term. Trusted regeneration plus expanded-KORE comparison is byte-identical (`04_program_pinning.log`). |
| F2/E1–E2 | 24–26 | `evenBit(Int):Int` (`function,total`), result 1 iff remainder is 0, else 0 | Complementary guards are disjoint and exhaustive; both equations are ordinary parity mathematics. |
| F3/E3–E4 | 28–30 | `countEven(PyList):Int` (`function,total`) | Nil/Cons equations are disjoint, exhaustive, and structurally decreasing; a definitional summary, not execution replacement. |
| F4/E5–E6 | 32–34 | `lastValue(PyList,Int):Int` (`function,total`) | Nil/Cons equations are disjoint, exhaustive, and structurally decreasing; truthfully summarizes the loop-variable cell. |

There are no local `functional`, opaque, priority, ordinary operational, or
explicit simplification rules in `verification.k`; M1/M2 are syntax macros and
F2–F4 are total equational functions.

## `spec.k`: claims

| ID | Lines | Claim |
|---|---:|---|
| C1 | 6–21 | `loop-counts-even`: arbitrary remaining list adds exactly `countEven(L)` and leaves the loop variable at `lastValue(L,OLD)`. |
| C2 | 23–35 | `exchange-yes`: full real program returns `"YES"` when total even count is at least `length(L1)`. |
| C3 | 37–49 | `exchange-no`: full real program returns `"NO"` when total even count is below `length(L1)`. |

The two entry guards are complementary over integer lists. C1 is the circular
loop invariant used by C2 and C3.
