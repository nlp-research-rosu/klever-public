requires "reference-semantics/semantics.k"
requires "solution-module.k"

module VERIFICATION-SYNTAX
  imports MPY-SYNTAX
  imports SOLUTION-MODULE-SYNTAX
  imports INT-SYNTAX
  imports BOOL-SYNTAX

  // Mathematical summaries used only in specifications and invariants.
  syntax Int ::= overlapLength(Int, Int, Int, Int) [function, total]
  syntax Bool ::= scanHasDivisor(Bool, Int, Int)
                  [function, total, no-evaluators]
  syntax Val ::= primeResult(Int) [function, total]
endmodule

module VERIFICATION
  imports MPY
  imports SOLUTION-MODULE
  imports VERIFICATION-SYNTAX
  imports INT
  imports BOOL

  rule overlapLength(A0, A1, B0, B1)
    => (#if B1 <Int A1 #then B1 #else A1 #fi)
       -Int (#if B0 >Int A0 #then B0 #else A0 #fi)

  // Ground definition. These disjoint cases cover every Bool/Int/Int input.
  // The only recursive case increases D toward N.
  rule scanHasDivisor(true, _N, _D) => true [concrete]
  rule scanHasDivisor(false, N, D) => scanHasDivisor(false, N, 2)
    requires D <Int 2
    [concrete]
  rule scanHasDivisor(false, N, D) => false
    requires D >=Int 2 andBool D >=Int N
    [concrete]
  rule scanHasDivisor(false, N, D) => true
    requires D >=Int 2 andBool D <Int N
         andBool pyMod(N, D) ==Int 0
    [concrete]
  rule scanHasDivisor(false, N, D)
    => scanHasDivisor(false, N, D +Int 1)
    requires D >=Int 2 andBool D <Int N
         andBool pyMod(N, D) =/=Int 0
    [concrete]

  // Symbolic consequences used by the loop proof. The fold rule matches only
  // the syntactic D + 1 created by one iteration and rewrites toward the
  // invariant's scan-at-D summary.
  rule scanHasDivisor(true, _N, _D) => true
    [simplification]
  rule scanHasDivisor(false, N, D) => false
    requires D >=Int 2 andBool D >=Int N
    [simplification]
  rule scanHasDivisor(false, N, D) => true
    requires D >=Int 2 andBool D <Int N
         andBool pyMod(N, D) ==Int 0
    [simplification]
  rule scanHasDivisor(false, N, D +Int 1)
    => scanHasDivisor(false, N, D)
    requires D >=Int 2 andBool D <Int N
         andBool pyMod(N, D) =/=Int 0
    [simplification]

  rule primeResult(N)
    => #if N <Int 2 orBool scanHasDivisor(false, N, 2)
       #then str(strToCodes("NO"))
       #else str(strToCodes("YES"))
       #fi
endmodule
