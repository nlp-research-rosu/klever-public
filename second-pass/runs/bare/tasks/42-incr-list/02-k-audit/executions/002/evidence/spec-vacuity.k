requires "verification.k"

module SPEC-VACUITY
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

  // False result mutation. The satisfying input L=[pyInt(0)] must return
  // pyList([pyInt(1)]), not an empty list.
  claim [incr-list-false-empty-result]:
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
      noResult => result(pyList(.List))
    </result>
    [depends(for-invariant)]
endmodule
