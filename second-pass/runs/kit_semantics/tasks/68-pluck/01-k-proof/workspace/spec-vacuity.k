requires "spec.k"

module SPEC-VACUITY
  imports SPEC

  // Deliberately false: when an even value exists, demand an index one larger
  // than the index computed by the target theorem.
  claim [pluck-entry-wrong-index]:
    <k>
      Call(Name("pluck"), list(INPUT:ValSeq))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      -1 |-> builtinsScope
      0  |-> scope(
        "pluck" |-> closureVal(
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
                  Compare(Name("value"), CmpOp("<", Name("smallest"))),
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
        parent(-1))
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      => 0 |-> resultList(
                  scanBest(INPUT, 0, -1),
                  scanBestIndex(INPUT, 0, -1, 0) +Int 1)
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires allNonNegative(INPUT)
endmodule
