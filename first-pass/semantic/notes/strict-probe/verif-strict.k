// verif-strict.k — probe: do strict/seqstrict (heat/cool freezers) disturb circularity
// proofs? A below-zero-shaped loop whose body computes through STRICT expressions:
// seqstrict binop, strict(1) ternary (the #branch analog: conditional match on a symbolic
// Bool). The invariant anchors at #sum — freezers live and die within one iteration.
module VERIF-STRICT
  imports INT
  imports BOOL
  imports K-EQUAL

  configuration <k> $PGM:K </k> <acc> 0 </acc>

  syntax Val ::= Int | Bool
  syntax KResult ::= Val

  syntax Exp ::= Val
               | add(Exp, Exp) [seqstrict]
               | lt(Exp, Exp)  [seqstrict]
               | ite(Exp, Exp, Exp) [strict(1)]
  rule add(I1:Int, I2:Int) => I1 +Int I2
  rule lt(I1:Int, I2:Int)  => I1 <Int I2
  rule ite(true,  T:Exp, _:Exp) => T
  rule ite(false, _:Exp, E:Exp) => E

  syntax ValSeq ::= ".ValSeq" | vCons(Int, ValSeq)

  // clampSum: acc' = -1 if acc+i < 0 else acc+i, folded over the list
  syntax KItem ::= #sum(ValSeq) | #store(ValSeq)
  rule <k> #sum(.ValSeq) => .K ... </k>
  rule <k> #sum(vCons(I:Int, R:ValSeq)) => ite(lt(add(A, I), 0), -1, add(A, I)) ~> #store(R) ... </k>
       <acc> A:Int </acc>
  rule <k> V:Int ~> #store(R:ValSeq) => #sum(R) ... </k>
       <acc> _ => V </acc>

  syntax Int ::= clampSum(ValSeq, Int) [function, total]
  rule clampSum(.ValSeq, A:Int) => A [simplification]
  rule clampSum(vCons(I:Int, R:ValSeq), A:Int) => clampSum(R, -1)
       requires A +Int I <Int 0 [simplification]
  rule clampSum(vCons(I:Int, R:ValSeq), A:Int) => clampSum(R, A +Int I)
       requires notBool (A +Int I <Int 0) [simplification]
endmodule
