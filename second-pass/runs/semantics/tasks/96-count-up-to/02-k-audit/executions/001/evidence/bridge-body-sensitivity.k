requires "source/verification.k"

// Operational-sensitivity test: change the displaced divisor-loop body so a
// found divisor assigns true rather than false, but retain the original result
// obligation. For N=5 this mutated loop appends 4, so the claim is false.
// Neither exact promoted bridge should match the mutated syntax.
module AUDIT-BRIDGE-BODY-SENSITIVITY-SPEC
  imports COUNT-UP-TO-WITH-OUTER

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
            Assign(Name("is_prime"), Bool(true)),
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
    </k>
    <env> 1 </env>
    <scopes>
      (0 |-> scope(.Map, parent(-1))
       -1 |-> builtinsScope
       1 |-> scope(
         ("n" |-> 5
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
