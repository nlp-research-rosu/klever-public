# Independent operational-bridge judgment

All four target parameters are bound to
`rule-9c06989c16c7a097c03e07267ceaa4fc5afd44c87f6099c4345fad7d4fc52617`.
The target invokes them only on the rule's complete guarded match domain:
`V` must be a string value, the method is exactly `"count"`, the argument list
contains exactly one string pattern, and its tail is empty.

## `isStringVal`

Frozen rules 79–80 return `true` exactly for `str(IntSeq)` values and use an
`owise` `false` rule for all other `Val` constructors. The candidate definition
`Operational.recognizesStringValue` matches `SortVal.inj_SortStr _` to `true`
and every other constructor to `false`. Ground Lean checks return `true` for a
string and `false` for an integer.

This guard is load-bearing. In the separate counterfactual workspace
`113-odd-count-mut-recognizer`, changing it to `fun _ => false` and changing
the proof to `cases h` makes the fixed target build successfully. That
mutation is mathematically vacuous and operationally false. The actual
candidate does not make this mutation: the string witness satisfies the real
guard, so `Proof.final` is not vacuous.

## `stringCodes`

Frozen rule 82 is the constructor projection
`stringCodes(str(CS)) => CS`. The candidate
`Operational.projectStringCodeSequence` returns the exact `codes` field from
the generated string constructor. Lean checks independently cover empty,
one-code, and two-code strings. Its arbitrary totalization to the empty
sequence for non-string values is outside the frozen rule's defined equation
and unreachable under the honest `isStringVal = true` hypothesis.

## `cntSub`

Frozen `methods.k` rules 36–39 implement a non-overlapping window scan:

- empty source returns zero;
- a nonempty pattern that prefixes the source contributes one and drops the
  pattern length;
- otherwise one source code is dropped;
- an empty pattern follows the non-prefix/zero-length branch until the source
  is empty, hence returns zero in this supplied semantics.

The candidate's `nonoverlapSubstringCount` uses source-length fuel. On every
reachable recursive call, the source loses at least one code, so the fuel
does not truncate a valid computation. Its empty-pattern shortcut has the
same value as the frozen recurrence. Independent ground outputs for
`([], [49])`, `([49,49,49], [])`, `([49,49,49], [49])`,
`([49,49,49], [49,49])`, and `([49,50,49,50], [49,50])` are respectively
`0, 0, 3, 1, 2`; an independently written Python reading of the K recurrence
produces the same vector.

In `113-odd-count-mut-cntsub`, replacing this definition by the convenient
constant `fun _ _ => 0` while keeping `applyMethod` honest makes the fixed
proof fail at the string case. This demonstrates that the target constrains
the result-bearing count function.

## `applyMethod`

The bound KORE symbol is the supplied `applyMethod(Val,String,Vals)` function.
The supplied string-count rule is
`applyMethod(str(CS), "count", str(PC), .Vals) => cntSub(CS, PC)`.
The candidate's `dispatchMethodMeaning`:

1. destructs the receiver as the exact generated string constructor;
2. selects method `"count"`;
3. requires the exact one-string argument plus empty `Vals` tail;
4. projects the receiver and pattern code sequences;
5. returns `SortVal.inj_SortInt (nonoverlapSubstringCount codes pattern)`.

This is the exact generated representation of the supplied rule. Ground Lean
checks return injected counts `2` and `3` for distinct strings, while a
non-string receiver and an unknown method return the candidate's off-relation
totalization rather than faking a count. The candidate also has explicit
branches for every other supplied `applyMethod` rule found in `methods.k`,
`tuple.k`, and `builtins.k`; `43_applyMethod_rule_coverage.txt` records the
rule/branch inventory. `Proof.final` uses only the count match domain above.

## Conclusion

The four definitions are not constant, identity, hard-coded-to-the-theorem, or
guard-vacuous on the generated obligation's domain. They implement the frozen
operational meaning needed by the domain lemma, and the source program's five
single-digit `s.count(...)` calls lie within that domain.
