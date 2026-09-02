# Satisfiable precondition witnesses

These are ground instances of every entry claim. Map keys not shown are absent.

## `prime-loop`

- `L = 1`, `N = 5`, `D = 2`, `B = true`, `REST = .Map`,
  `SC = 0 |-> scope(.Map, parent(-1))`, `P = parent(0)`, `K = .K`.
- The guards hold: `2 >= 2`, `N >= 2`, and the four excluded keys are absent.
- Fixed execution tests divisors beginning at `2`; the summary is
  `trialPrime(5,2,true) = true`, `trialDivisor(5,2,true) = 3`.

## `digit-loop`

- `L = 1`, `N = 101`, `A = 0`, `REST = .Map`,
  `SC = 0 |-> scope(.Map, parent(-1))`, `P = parent(0)`, `K = .K`.
- The guards hold: `101 >= 0` and the excluded keys are absent.
- The post-state is `largest = 0`, `digit_total = digitAcc(101,0) = 2`.

## `scan-loop`

- `S = 1`, `CALLER = 0`, `CONT = .K`,
  `IS = intCons(2,intCons(4,intCons(11,.IntList)))`, `CUR = 0`,
  `OLDN = 0`, `OLDD = 2`, `OLDB = false`.
- `REST = "lst" |-> list(asVals(IS))`,
  `BASE = 0 |-> scope(.Map,parent(-1))`, and the callee parent is `parent(0)`.
- The complete stack is `ListItem(frame(.K,0,1))`; `scopeLoc = 2`;
  the required `ret` is `noRet`.
- All exclusions hold and location `1` is absent from `BASE`.
- The result is `digitSum(largestPrime(IS,0)) = 2`.

## `entry-prefix`

- `IS = intCons(2,intCons(4,intCons(11,.IntList)))`.
- `MOD = 0 |-> scope(.Map,parent(-1)) -1 |-> builtinsScope`;
  location `1` is absent, `env = 0`, `scopeLoc = 1`, stack is empty, and
  `ret = noRet`.
- The result is `2`.

## `main-correct`

- The claim itself fixes the complete initial configuration. Choose
  `IS = intCons(2,intCons(4,intCons(11,.IntList)))`; the formal result is `2`.
  Both `/tmp/audit-work/trusted/canonical.py` and
  `/tmp/audit-work/reconstruction/solution.py` return `2`.
- The formal domain also admits `IS = intCons(1,.IntList)`. The formal summary
  and generated implementation return `0`; the trusted canonical implementation
  returns `1`. This is the independently recorded canonical `1`-as-prime
  discrepancy, not a failed precondition.
