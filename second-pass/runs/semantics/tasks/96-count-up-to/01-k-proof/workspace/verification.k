requires "reference-semantics/semantics.k"

// Mathematical definitions and the unmodified Python semantics.
module COUNT-UP-TO-BASE
  imports MPY

  // noDivisor(C, D, HI) says that none of D, D+1, ..., HI-1
  // divides C.  All calls made by the program satisfy 2 <= D <= HI.
  syntax Bool ::= noDivisor(Int, Int, Int)
    [function, total, symbol(noDivisor), no-evaluators]
  rule noDivisor(_:Int, D:Int, HI:Int) => true
    requires D >=Int HI
  rule noDivisor(C:Int, D:Int, HI:Int) => false
    requires D <Int HI andBool pyMod(C, D) ==Int 0
  rule noDivisor(C:Int, D:Int, HI:Int)
    => noDivisor(C, D +Int 1, HI)
    requires D <Int HI andBool pyMod(C, D) =/=Int 0

  // Append I exactly when the divisor scan establishes that I is prime.
  syntax ValSeq ::= appendIfPrime(ValSeq, Int, Bool)
    [function, total, symbol(appendIfPrime), no-evaluators]
  rule appendIfPrime(VS:ValSeq, _:Int, false) => VS
  rule appendIfPrime(VS:ValSeq, I:Int, true)
    => valSeqConcat(VS, vCons(I, .ValSeq))

  // primesAcc(VS, I, N) is VS followed by every prime in [I, N), in
  // increasing order.  Since all reachable I are at least 2, primality is
  // exactly noDivisor(I, 2, I).
  syntax ValSeq ::= primesAcc(ValSeq, Int, Int)
    [function, total, symbol(primesAcc), no-evaluators]
  rule primesAcc(VS:ValSeq, I:Int, N:Int) => VS
    requires I >=Int N
  rule primesAcc(VS:ValSeq, I:Int, N:Int)
    => primesAcc(
         appendIfPrime(VS, I, noDivisor(I, 2, I)),
         I +Int 1,
         N)
    requires I <Int N
endmodule

// This module adds the inner-loop theorem as a reusable semantic rule.  The
// corresponding claim is proved against COUNT-UP-TO-BASE alone in spec.k.
module COUNT-UP-TO-WITH-INNER
  imports COUNT-UP-TO-BASE

  rule <k>
         #while(
           Compare(Name("divisor"), CmpOp("<", Name("candidate"))),
           If(
             Compare(
               BinOp("%", Name("candidate"), Name("divisor")),
               CmpOp("==", Int(0))),
             Assign(Name("is_prime"), Bool(false)),
             .Stmts)
           AugAssign(Name("divisor"), "+", Int(1)))
         => .K
         ...
       </k>
       <env> 1 </env>
       <scopes>
         0 |-> scope(MOD:Map, parent(-1))
         -1 |-> scope(BI:Map, root)
         1 |-> scope(
           ("candidate" |-> C:Int
            "divisor" |-> (D:Int => C)
            "is_prime" |-> (B:Bool => B andBool noDivisor(C, D, C))
            "n" |-> N:Int
            "result" |-> ref(0)),
           parent(0))
       </scopes>
       <heap> 0 |-> list(VS:ValSeq) </heap>
       requires 2 <=Int D andBool D <=Int C
       [priority(40)]
endmodule

// This module adds the outer-loop theorem as a reusable semantic rule.  Its
// claim is proved against COUNT-UP-TO-WITH-INNER, so the only trusted layer at
// that stage is the already-proved inner-loop theorem.
module COUNT-UP-TO-WITH-OUTER
  imports COUNT-UP-TO-WITH-INNER

  rule <k>
         #while(
           Compare(Name("candidate"), CmpOp("<", Name("n"))),
           While(
             Compare(Name("divisor"), CmpOp("<", Name("candidate"))),
             If(
               Compare(
                 BinOp("%", Name("candidate"), Name("divisor")),
                 CmpOp("==", Int(0))),
               Assign(Name("is_prime"), Bool(false)),
               .Stmts)
             AugAssign(Name("divisor"), "+", Int(1)))
           If(
             Name("is_prime"),
             Expr(Call(
               Attribute(Name("result"), "append"),
               Name("candidate"))),
             .Stmts)
           AugAssign(Name("candidate"), "+", Int(1))
           Assign(Name("is_prime"), Bool(true))
           Assign(Name("divisor"), Int(2)))
         => .K
         ...
       </k>
       <env> 1 </env>
       <scopes>
         0 |-> scope(MOD:Map, parent(-1))
         -1 |-> scope(BI:Map, root)
         1 |-> scope(
           ("n" |-> N:Int
            "candidate" |-> (I:Int => N)
            "is_prime" |-> true
            "divisor" |-> 2
            "result" |-> ref(0)),
           parent(0))
       </scopes>
       <heap>
         0 |-> (list(VS:ValSeq) => list(primesAcc(VS, I, N)))
       </heap>
       requires 2 <=Int I andBool I <=Int N
       [priority(40)]
endmodule
