# Satisfying witnesses and concrete result substitution

All maps below omit the named keys from their `REST`/`BASE` fragments.  Empty
maps therefore satisfy every `notBool (... in_keys(...))` side condition.

## `prime-loop`

- `N = 2`, `D = 2`, `B = true`, `L = 1`, `REST = .Map`,
  `SC = .Map`, `P = parent(0)`, `K = .K`.
- `D >= 2` and `(not B or N >= 2)` are true; all key-exclusion guards are
  true.
- The source loop guard is false because `2 * 2 > 2`.  Both
  `trialPrime(2,2,true)` and the concrete local `prime` are `true`;
  `trialDivisor(2,2,true) = 2`.

## `digit-loop`

- `N = 2`, `A = 0`, `L = 1`, `REST = .Map`, `SC = .Map`,
  `P = parent(0)`, `K = .K`.
- `N >= 0` and every key-exclusion guard are true.
- One source iteration yields `largest = 0`, `digit_total = 2`;
  `digitAcc(2,0) = 2`.

## `scan-loop`

- `IS = intCons(2, .IntList)`, `CUR = 0`, `S = 1`, `CALLER = 0`,
  `OLDN = 0`, `OLDD = 2`, `OLDB = false`, `REST = .Map`,
  `BASE = 0 |-> scope(.Map, parent(-1))`, `CONT = .K`,
  `STACK = .List`.
- `CUR >= 0`, key exclusions, and `notBool (S in_keys(BASE))` all hold.
- The loop finds largest prime `2`; the digit loop returns `2`; the function
  frame is popped back to caller environment `0`.

## `entry-prefix`

- `IS = intCons(2, .IntList)`.
- `MOD = 0 |-> scope(.Map, parent(-1))
  -1 |-> builtinsScope`, so location `1` is absent.
- The claimed result is
  `digitSum(largestPrime(intCons(2,.IntList),0)) = 2`.

## `main-correct`

- `IS = intCons(2, .IntList)` in the claim's fully concrete initial
  configuration.
- The claim has no additional `requires`; that configuration is realizable.
- Submitted Python returns `2`, trusted canonical Python returns `2`, the
  independent mathematical oracle returns `2`, and the K postcondition
  reduces to `2`.

The concrete substitution is recorded by `02-differential.log` (boundary case
`[2]`) and by `06-vacuity-witness.log`.
