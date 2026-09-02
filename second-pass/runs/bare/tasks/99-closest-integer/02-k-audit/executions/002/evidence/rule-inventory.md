# Independent local K inventory

Line references are to the immutable candidate copies in `/candidate`.

## Syntax, attributes, configuration

`semantic.k` declares:

- `Program`: `Module(Stmts)` (line 5).
- `Stmts`: zero-separator list of `Stmt` (line 7).
- `Stmt`: `ImportFrom`, `FuncDef`, `Assign`, `If`, and `Return` (lines 8–12).
- `Params`: one string parameter (line 14).
- `Expr`: `Name`, `Int`, `Str`, `Call`, `BinOp`, and `Compare` (lines 16–21).
- `CmpOp`: operator string plus right expression (line 23).
- `Value`: `pyInt`, `pyStr`, `pyBool`, `exactNum`, and `rationalString`
  (lines 37–41).
- `Result`: `noResult` or `Value` (line 43).
- `KItem`: `exec`, `assignTo`, `toDecimal`, `toInt`, `ifControl`,
  `binLeft`, `binRight`, `compareLeft`, `compareRight`, and
  `returnControl` (lines 45–54).
- Configuration: `<k>`, `<arg>`, `<env>`, and `<result>` under `<mpy>`
  (lines 56–62). These cells are all read or written.
- Functional symbols: `exponentPosition` (also `[total]`), `parseDecimal`,
  `parseExponent`, `parseMantissa`, `parseMantissaAt`, and `scaleDecimal`
  (lines 121 and 127–131).

`verification.k` adds functional `solutionProgram` (line 8) and functional
`roundNearestAway` (line 24).

There are no `[simplification]`, `[simplify]`, `[priority]`, `[owise]`,
`[opaque]`, `[functional]`, or local macro declarations. There are no local
helper K files beyond `semantic.k` and `verification.k`. `rationalString` is an
ordinary constructor, but it is a result-bearing abstract input with no
connection claim to `pyStr`.

## Operational and equational rules

| ID | Candidate lines | Rule and review |
|---|---:|---|
| S1 | semantic.k 65–69 | Exact `Module(ImportFrom(decimal.Decimal), FuncDef(closest_integer,...))` loader initializes the parameter and executes the body. Sound for the submitted one-function module; intentionally not general Python import/call semantics. |
| S2 | 72 | Empty statement list completes. Sound. |
| S3 | 73 | Head/tail statement sequencing. Sound. |
| S4 | 74 | Assignment evaluates its RHS before update. Sound for the used `Name` target. |
| S5 | 75–76 | Commits a value to the map. Sound. |
| S6 | 79 | Integer literal to `pyInt`. Sound. |
| S7 | 80 | String literal to `pyStr`. Sound. |
| S8 | 81–82 | Environment lookup. Sound when the binding exists; otherwise visibly stuck. |
| S9 | 85 | Textual `Decimal` call evaluates its argument then uses `toDecimal`. Sound on the exact submitted body after S1, but over-broad as reusable Python because it bypasses general binding lookup. |
| S10 | 86 | `pyStr(S) ~> toDecimal => parseDecimal(S)`. **Unsound over the real program's accepted string domain.** Witness `S = " 2.5 "`: Python `Decimal` denotes 5/2 and the submitted program returns 3, while these equations produce 25/100 and final result 0. Witness `S = "1_000.5"`: Python returns 1001, while K aborts in `String2Int`. See `03-semantic-differential.log`. |
| S11 | 87 | `rationalString(N,D)` converts directly to `exactNum(N,D)`. Truthful only as a named abstract-input contract; it is a result-bearing operational bridge and is not a theorem about any actual `pyStr(S)`. The universal spec depends on it. |
| S12 | 88 | Textual `int` call evaluates argument then uses `toInt`. Sound on the submitted body; over-broad for hypothetical shadowing. |
| S13 | 89 | `int(pyInt(I)) = pyInt(I)`. Sound. |
| S14 | 90–91 | `int(exactNum(N,D)) = N /Int D` for positive D. Sound because K `/Int` and Python `int(Decimal)` both truncate toward zero. Concrete positive/negative witnesses passed. |
| S15 | 94 | Begins left-to-right binary evaluation. Sound. |
| S16 | 95 | Evaluates the right operand after the left value. Sound. |
| S17 | 96–98 | Exact rational addition for positive denominators. Sound by cross multiplication. |
| S18 | 99–101 | Exact rational subtraction for positive denominators. Sound by cross multiplication. |
| S19 | 103–104 | Begins comparison evaluation with the left side. Sound. |
| S20 | 105–106 | Evaluates comparison right side second. Sound. |
| S21 | 107–109 | `exactNum(N1,D1) >= pyInt(I2)` via `N1 >= I2*D1`, D1>0. Sound. |
| S22 | 112 | Evaluates an `If` guard before branch selection. Sound. |
| S23 | 113 | True guard executes the then list. Sound. |
| S24 | 114 | False guard executes the else list. Sound. |
| S25 | 115 | Evaluates a return expression. Sound. |
| S26 | 116–117 | Return stores the value and discards the remaining function continuation. Sound for the one active function. The positive-branch concrete cases verify that the trailing negative return is discarded. |
| S27 | 122–123 | `exponentPosition` chooses lowercase `e` when present. Sound. |
| S28 | 124–125 | Otherwise chooses uppercase `E`. Guard-disjoint with S27 and completes the `[total]` definition for all strings. |
| S29 | 133–134 | No exponent means parse the mantissa. Sound as routing. |
| S30 | 135–136 | An exponent position routes to `parseExponent`. Sound as routing. |
| S31 | 137–140 | Parses mantissa and exponent and scales. Correct for the tested ordinary scientific grammar; it does not validate the full `Decimal` lexical domain before partial `String2Int` hooks. |
| S32 | 142–143 | Dot-free mantissa becomes integer/1. Correct for digit/sign strings; partial or wrong outside that unstated grammar. |
| S33 | 144–145 | A dotted mantissa routes to the first dot. Sound as routing. |
| S34 | 146–151 | Removes the dot and uses total string length to select a power-of-ten denominator. **Unsound on valid whitespace-bearing inputs** because whitespace is counted as fractional digits while `String2Int` trims it. False conclusion witness: `parseMantissaAt(" 2.5 ",2) => exactNum(25,100)` although Python `Decimal(" 2.5 ") = 5/2`; this enables final 0 instead of 3. It also sends valid underscore notation to a partial hook and crashes. |
| S35 | 153–154 | Nonnegative decimal exponent scales numerator by 10^E. Sound. |
| S36 | 155–156 | Negative exponent scales denominator by 10^(-E). Sound. |
| V1 | verification.k 9–20 | `solutionProgram` expands to the exact submitted constructor term. Independent KAST comparison after only empty-list spelling normalization produced equal hashes; see `04-program-term-compare.log`. |
| V2 | 25–27 | For N>=0,D>0, add half then truncate: `(10N+5D)/(10D)`. Sound and matches execution. |
| V3 | 28–30 | For N<0,D>0, subtract half then truncate: `(10N-5D)/(10D)`. Sound and matches execution. The guards are disjoint and cover every N under D>0. |

## Submitted reachability claims

`spec.k` contains eleven positive claims:

1. All abstract `rationalString(N,D)` values with D>0 return
   `roundNearestAway(N,D)`.
2. All positive half ties `(2I+1)/2`, I>=0, return I+1.
3. All negative half ties `-(2I+1)/2`, I>=0, return -(I+1).
4. Positive `(4I+1)/4`, I>=0, returns I.
5. Positive `(4I+3)/4`, I>=0, returns I+1.
6. Negative `-(4I+1)/4`, I>=0, returns -I.
7. Negative `-(4I+3)/4`, I>=0, returns -(I+1).
8–11. Ground `pyStr` examples `"10"`, `"15.3"`, `"14.5"`, and
`"-14.5"`.

All postconditions fix `<result>` to a specific `pyInt`; none is a tautology or
free-result claim. Claims 1–7 quantify abstract numeric inputs, not real source
strings. Claims 8–11 are the only submitted theorems whose precondition
contains an actual `pyStr`.

## Construct coverage for `solution.mpy`

- `Module`, `ImportFrom`, `FuncDef`, and `Params`: S1.
- Statement lists: S2–S3.
- `Assign`: S4–S5.
- `Name`, `Int`, and `Str`: S6–S8.
- `Call(Decimal,...)` and `Call(int,...)`: S9–S14 plus parsing S27–S36.
- `BinOp(+/-)`: S15–S18.
- `Compare(>=)`: S19–S21.
- `If`: S22–S24.
- `Return`: S25–S26.

Every constructor in the submitted term has a rule path. The material defect is
not a missing AST constructor: it is that the used `Decimal` string conversion
path is false or partial for accepted real-program inputs, while the universal
proof bypasses that path using S11.
