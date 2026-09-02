requires "source/verification.k"

// Bridge-free universal connection theorem over the complete match domain of
// verification.k's promoted inner-loop rule, including arbitrary omitted cells
// and arbitrary trailing K.
module AUDIT-INNER-BRIDGE-DOMAIN-SPEC
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
endmodule

// Bridge-free universal connection theorem over the complete match domain of
// the promoted outer-loop rule. It uses only the independently validated inner
// bridge, not the proposed outer bridge.
module AUDIT-OUTER-BRIDGE-DOMAIN-SPEC
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
endmodule

// Ground fixed-semantics witness with an observable immediate continuation.
module AUDIT-INNER-CONTEXT-FIXED-SPEC
  imports COUNT-UP-TO-BASE

  claim
    <k>
      (#while(
        Compare(Name("divisor"), CmpOp("<", Name("candidate"))),
        If(
          Compare(
            BinOp("%", Name("candidate"), Name("divisor")),
            CmpOp("==", Int(0))),
          Assign(Name("is_prime"), Bool(false)),
          .Stmts)
        AugAssign(Name("divisor"), "+", Int(1)))
      ~> Assign(Name("n"), Int(99)))
      => .K
    </k>
    <env> 1 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope
       1 |-> scope(
         ("candidate" |-> 4
          "divisor" |-> (2 => 4)
          "is_prime" |-> (true => false)
          "n" |-> (5 => 99)
          "result" |-> ref(0)),
         parent(0)))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> 0 |-> list(.ValSeq) </heap>
    <heapLoc> 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
endmodule

module AUDIT-INNER-CONTEXT-EXTENDED-SPEC
  imports COUNT-UP-TO-WITH-INNER

  claim
    <k>
      (#while(
        Compare(Name("divisor"), CmpOp("<", Name("candidate"))),
        If(
          Compare(
            BinOp("%", Name("candidate"), Name("divisor")),
            CmpOp("==", Int(0))),
          Assign(Name("is_prime"), Bool(false)),
          .Stmts)
        AugAssign(Name("divisor"), "+", Int(1)))
      ~> Assign(Name("n"), Int(99)))
      => .K
    </k>
    <env> 1 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope
       1 |-> scope(
         ("candidate" |-> 4
          "divisor" |-> (2 => 4)
          "is_prime" |-> (true => false)
          "n" |-> (5 => 99)
          "result" |-> ref(0)),
         parent(0)))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap> 0 |-> list(.ValSeq) </heap>
    <heapLoc> 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
endmodule

module AUDIT-OUTER-CONTEXT-FIXED-SPEC
  imports COUNT-UP-TO-BASE

  claim
    <k>
      (#while(
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
      ~> Assign(Name("n"), Int(99)))
      => .K
    </k>
    <env> 1 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope
       1 |-> scope(
         ("n" |-> (5 => 99)
          "candidate" |-> (2 => 5)
          "is_prime" |-> true
          "divisor" |-> 2
          "result" |-> ref(0)),
         parent(0)))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap>
      0 |-> (list(.ValSeq)
        => list(vCons(2, vCons(3, .ValSeq))))
    </heap>
    <heapLoc> 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
endmodule

module AUDIT-OUTER-CONTEXT-EXTENDED-SPEC
  imports COUNT-UP-TO-WITH-OUTER

  claim
    <k>
      (#while(
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
      ~> Assign(Name("n"), Int(99)))
      => .K
    </k>
    <env> 1 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope
       1 |-> scope(
         ("n" |-> (5 => 99)
          "candidate" |-> (2 => 5)
          "is_prime" |-> true
          "divisor" |-> 2
          "result" |-> ref(0)),
         parent(0)))
    </scopes>
    <scopeLoc> 2 </scopeLoc>
    <heap>
      0 |-> (list(.ValSeq)
        => list(vCons(2, vCons(3, .ValSeq))))
    </heap>
    <heapLoc> 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
endmodule
