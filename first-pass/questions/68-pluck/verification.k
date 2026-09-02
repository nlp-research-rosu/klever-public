// verification.k — pluck on the UNIFIED semantics (109-style kit: Val-arg
// folds, casts in the GUARDS only, guarded Bool handling — no literal Bool
// patterns, no knownIntP layer, no local echoes).

requires "../../reference/src/lemmas.k"

module PLUCK-VERIFICATION
  imports MPY-LEMMAS
  imports MAP-SYMBOLIC

  syntax Expr ::= Val

  syntax Bool ::= pFound(ValSeq, Bool, Val, Int, Int) [function, total]
  rule pFound(.ValSeq, F:Bool, _BV:Val, _BI:Int, _I:Int) => F [simplification]
  rule pFound(vCons(V:Val, S:ValSeq), F:Bool, _BV:Val, _BI:Int, I:Int)
    => pFound(S, true, V, I, I +Int 1)
    requires notBool F andBool projectIntTotal(V) modInt 2 ==Int 0 [simplification]
  rule pFound(vCons(V:Val, S:ValSeq), F:Bool, BV:Val, _BI:Int, I:Int)
    => pFound(S, true, V, I, I +Int 1)
    requires F andBool projectIntTotal(V) modInt 2 ==Int 0
     andBool projectIntTotal(V) <Int projectIntTotal(BV) [simplification]
  rule pFound(vCons(V:Val, S:ValSeq), F:Bool, BV:Val, BI:Int, I:Int)
    => pFound(S, F, BV, BI, I +Int 1)
    requires F andBool projectIntTotal(V) modInt 2 ==Int 0
     andBool notBool (projectIntTotal(V) <Int projectIntTotal(BV)) [simplification]
  rule pFound(vCons(V:Val, S:ValSeq), F:Bool, BV:Val, BI:Int, I:Int)
    => pFound(S, F, BV, BI, I +Int 1)
    requires notBool (projectIntTotal(V) modInt 2 ==Int 0) [simplification]

  syntax Val ::= pBest(ValSeq, Bool, Val, Int, Int) [function, total]
  rule pBest(.ValSeq, _F:Bool, BV:Val, _BI:Int, _I:Int) => BV [simplification]
  rule pBest(vCons(V:Val, S:ValSeq), F:Bool, _BV:Val, _BI:Int, I:Int)
    => pBest(S, true, V, I, I +Int 1)
    requires notBool F andBool projectIntTotal(V) modInt 2 ==Int 0 [simplification]
  rule pBest(vCons(V:Val, S:ValSeq), F:Bool, BV:Val, _BI:Int, I:Int)
    => pBest(S, true, V, I, I +Int 1)
    requires F andBool projectIntTotal(V) modInt 2 ==Int 0
     andBool projectIntTotal(V) <Int projectIntTotal(BV) [simplification]
  rule pBest(vCons(V:Val, S:ValSeq), F:Bool, BV:Val, BI:Int, I:Int)
    => pBest(S, F, BV, BI, I +Int 1)
    requires F andBool projectIntTotal(V) modInt 2 ==Int 0
     andBool notBool (projectIntTotal(V) <Int projectIntTotal(BV)) [simplification]
  rule pBest(vCons(V:Val, S:ValSeq), F:Bool, BV:Val, BI:Int, I:Int)
    => pBest(S, F, BV, BI, I +Int 1)
    requires notBool (projectIntTotal(V) modInt 2 ==Int 0) [simplification]

  syntax Int ::= pIdx(ValSeq, Bool, Val, Int, Int) [function, total]
  rule pIdx(.ValSeq, _F:Bool, _BV:Val, BI:Int, _I:Int) => BI [simplification]
  rule pIdx(vCons(V:Val, S:ValSeq), F:Bool, _BV:Val, _BI:Int, I:Int)
    => pIdx(S, true, V, I, I +Int 1)
    requires notBool F andBool projectIntTotal(V) modInt 2 ==Int 0 [simplification]
  rule pIdx(vCons(V:Val, S:ValSeq), F:Bool, BV:Val, _BI:Int, I:Int)
    => pIdx(S, true, V, I, I +Int 1)
    requires F andBool projectIntTotal(V) modInt 2 ==Int 0
     andBool projectIntTotal(V) <Int projectIntTotal(BV) [simplification]
  rule pIdx(vCons(V:Val, S:ValSeq), F:Bool, BV:Val, BI:Int, I:Int)
    => pIdx(S, F, BV, BI, I +Int 1)
    requires F andBool projectIntTotal(V) modInt 2 ==Int 0
     andBool notBool (projectIntTotal(V) <Int projectIntTotal(BV)) [simplification]
  rule pIdx(vCons(V:Val, S:ValSeq), F:Bool, BV:Val, BI:Int, I:Int)
    => pIdx(S, F, BV, BI, I +Int 1)
    requires notBool (projectIntTotal(V) modInt 2 ==Int 0) [simplification]

endmodule
