requires "verification.k"

module SPEC-BODY-MUTATION
  imports VERIFICATION

  claim [for-invariant]:
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
    <iter>
      _IT => ?_
    </iter>
    <result>
      noResult => result(#incPrefix(L, size(L)))
    </result>
    requires (0 <=Int I) andBool (I <=Int size(L))

  // Body-sensitivity mutation: the submitted entry body now adds 2, while
  // both the auxiliary claim and requested summary still describe adding 1.
  claim [incr-list-body-adds-two]:
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
                  ListExpr(BinOp("+", Name("value"), Int(2))))))
            Return(Name("result")))),
        pyList(L))
      => .K
    </k>
    <env>
      .Map => ?_
    </env>
    <iter>
      noIter => ?_
    </iter>
    <result>
      noResult => result(#incPrefix(L, size(L)))
    </result>
    [depends(for-invariant)]
endmodule
