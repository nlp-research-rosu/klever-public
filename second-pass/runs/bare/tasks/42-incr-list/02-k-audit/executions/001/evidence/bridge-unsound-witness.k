requires "verification.k"

module BRIDGE-UNSOUND-WITNESS
  imports VERIFICATION

  // Candidate invariant copied exactly apart from its label.
  claim [for-invariant-witness]:
    <k>
      #for(
        L,
        I,
        "value",
        Assign(
          Name("result"),
          BinOp(
            "+",
            Name("result"),
            ListExpr(BinOp("+", Name("value"), Int(1))))))
      ~> #exec(Return(Name("result")))
      => .K
    </k>
    <env>
      "l" |-> pyList(L)
      "result" |-> (#incPrefix(L, I) => #incPrefix(L, size(L)))
    </env>
    <iter> _IT => ?_ </iter>
    <result>
      noResult => result(#incPrefix(L, size(L)))
    </result>
    requires (0 <=Int I) andBool (I <=Int size(L))

  // This satisfies the candidate entry claim's unrestricted pyList(L)
  // precondition, but Python cannot add 1 to the nested empty list.
  claim [nested-list-false-return]:
    <k>
      #init(
        Module(
          FuncDef("incr_list", Params("l"),
            Assign(Name("result"), ListExpr(.Exps))
            For(Name("value"), Name("l"),
              Assign(
                Name("result"),
                BinOp(
                  "+",
                  Name("result"),
                  ListExpr(BinOp("+", Name("value"), Int(1))))))
            Return(Name("result")))),
        pyList(ListItem(pyList(.List))))
      => .K
    </k>
    <env> .Map => ?_ </env>
    <iter> noIter => ?_ </iter>
    <result>
      noResult
      => result(#incPrefix(ListItem(pyList(.List)), 1))
    </result>
    [depends(for-invariant-witness)]
endmodule
