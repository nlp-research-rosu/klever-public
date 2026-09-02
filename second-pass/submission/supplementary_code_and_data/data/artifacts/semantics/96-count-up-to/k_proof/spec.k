requires "verification.k"

// Lemma 1: scanning the possible divisors updates is_prime to the conjunction
// of its incoming value and the mathematical no-divisor predicate.
module COUNT-UP-TO-INNER-LOOP-SPEC
  imports COUNT-UP-TO-BASE

  claim
    <k>
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
      -1 |-> builtinsScope
      1 |-> scope(
        ("candidate" |-> C:Int
         "divisor" |-> (D:Int => C)
         "is_prime" |-> (B:Bool => B andBool noDivisor(C, D, C))
         "n" |-> N:Int
         "result" |-> ref(0)),
        parent(0))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> 0 |-> list(VS:ValSeq) </heap>
    <heapLoc> 1 </heapLoc>
    <stack> ST:List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    requires 2 <=Int D andBool D <=Int C
endmodule

// Lemma 2: starting with a prefix VS at candidate I, the outer loop appends
// exactly the increasing prime sequence in [I, N).
module COUNT-UP-TO-OUTER-LOOP-SPEC
  imports COUNT-UP-TO-WITH-INNER

  claim
    <k>
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
      -1 |-> builtinsScope
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
    <scopeLoc> 2 </scopeLoc>
    <heapLoc> 1 </heapLoc>
    <stack> ST:List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    requires 2 <=Int I andBool I <=Int N
endmodule

// The entry-body theorem uses only the two preceding, independently proved
// loop lemmas.  primesAcc(.ValSeq, 2, N) is the formal contract result.
module COUNT-UP-TO-ENTRY-SPEC
  imports COUNT-UP-TO-WITH-OUTER

  claim
    <k>
      Assign(Name("result"), ListExpr(.Exprs))
      Assign(Name("candidate"), Int(2))
      Assign(Name("is_prime"), Bool(true))
      Assign(Name("divisor"), Int(2))
      While(
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
      Return(Name("result"))
      ~> #endcall
    => ref(0)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope
       1 |-> scope("n" |-> N:Int, parent(0)))
    =>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map => 0 |-> list(primesAcc(.ValSeq, 2, N)) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    requires N >=Int 2
endmodule

// The n < 2 boundary is a separate claim because the outer-loop lemma's
// induction domain starts at candidate 2.  The contract result is empty.
module COUNT-UP-TO-BOUNDARY-SPEC
  imports COUNT-UP-TO-WITH-OUTER

  claim
    <k>
      Assign(Name("result"), ListExpr(.Exprs))
      Assign(Name("candidate"), Int(2))
      Assign(Name("is_prime"), Bool(true))
      Assign(Name("divisor"), Int(2))
      While(
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
      Return(Name("result"))
      ~> #endcall
    => ref(0)
    </k>
    <env> 1 => 0 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope
       1 |-> scope("n" |-> N:Int, parent(0)))
    =>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope)
    </scopes>
    <scopeLoc> 2 => 1 </scopeLoc>
    <heap> .Map => 0 |-> list(.ValSeq) </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> ListItem(frame(.K, 0, 1)) => .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    requires 0 <=Int N andBool N <Int 2
endmodule
