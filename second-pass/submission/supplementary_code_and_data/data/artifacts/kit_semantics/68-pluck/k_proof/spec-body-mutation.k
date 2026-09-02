requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  // Deliberately mutated source body: "value < smallest" is changed to
  // "value > smallest".  On [4, 2, 3] this returns [4, 0], so the original
  // expected [2, 1] must be rejected.
  claim [mutated-body-rejected]:
    <k>
      Call(
        closureVal(
          "arr",
          Assign(Name("smallest"), UnaryOp("-", Int(1)))
          Assign(Name("smallest_index"), Int(0))
          Assign(Name("index"), Int(0))
          Assign(Name("value"), Int(0))
          For(
            Name("value"),
            Name("arr"),
            Assign(Name("value"), BinOp("+", Name("value"), Int(0)))
            If(
              Compare(
                BinOp("%", Name("value"), Int(2)),
                CmpOp("==", Int(0))),
              If(
                Compare(Name("smallest"), CmpOp("<", Int(0))),
                Assign(Name("smallest"), Name("value"))
                Assign(Name("smallest_index"), Name("index")),
                If(
                  Compare(Name("value"), CmpOp(">", Name("smallest"))),
                  Assign(Name("smallest"), Name("value"))
                  Assign(Name("smallest_index"), Name("index")),
                  .Stmts)),
              .Stmts)
            AugAssign(Name("index"), "+", Int(1)))
          If(
            Compare(Name("smallest"), CmpOp("<", Int(0))),
            Return(ListExpr(.Exprs)),
            .Stmts)
          Return(ListExpr(Name("smallest"), Name("smallest_index"))),
          0),
        list(vCons(4, vCons(2, vCons(3, .ValSeq)))))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0  |-> scope(.Map, parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      => 0 |-> list(vCons(2, vCons(1, .ValSeq)))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
endmodule
