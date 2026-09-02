requires "verification.k"

module SPEC-BODY-AUDIT
  imports VERIFICATION

  claim [min-float-loop]:
    <k> #minAccF(list(VS:ValSeq), M:Float)
      => minTailF(VS, M) ... </k>
    requires allFloatVS(VS)

  claim [max-float-loop]:
    <k> #maxAccF(list(VS:ValSeq), M:Float)
      => maxTailF(VS, M) ... </k>
    requires allFloatVS(VS)

  claim [scale-loop]:
    <k>
      #loop(
        list(VS:ValSeq),
        Name("number"),
        Expr(
          Call(
            Attribute(Name("result"), "append"),
            BinOp(
              "/",
              BinOp("-", Name("number"), Name("min_number")),
              BinOp("-", Name("max_number"), Name("min_number"))))))
      => .K
      ...
    </k>
    <env> L:Int </env>
    <scopes>
      ...
      L |-> scope(
        ( "number"     |-> (CURRENT:Val => lastVal(VS, CURRENT))
          "numbers"    |-> list(ORIGINAL:ValSeq)
          "result"     |-> ref(H:Int)
          "min_number" |-> LO:Float
          "max_number" |-> HI:Float ),
        P:Parent)
      ...
    </scopes>
    <heap>
      ...
      H |-> list(
        ACC:ValSeq
        => scaleAcc(ACC, VS, LO, HI))
      ...
    </heap>
    requires allFloatVS(VS)

  claim [rescale-to-unit]:
    <k>
      #loadAll(
        Module(
          ImportFrom("typing", "List")
          FuncDef(
            "rescale_to_unit",
            Params("numbers"),
            Assign(
              Name("min_number"),
              Call(Name("min"), Name("numbers")))
            Assign(
              Name("max_number"),
              Call(Name("max"), Name("numbers")))
            Assign(Name("result"), ListExpr(.Exprs))
            Assign(
              Name("number"),
              Subscript(Name("numbers"), Int(0)))
            For(
              Name("number"),
              Name("numbers"),
              Expr(
                Call(
                  Attribute(Name("result"), "append"),
                  BinOp(
                    "/",
                    BinOp("-", Name("number"), Name("min_number")),
                    BinOp("-", Name("max_number"), Name("min_number"))))))
            Return(Name("numbers")))))
      ~> Call(
           Name("rescale_to_unit"),
           list(vCons(FIRST:Float,
                 vCons(SECOND:Float, REST:ValSeq))))
      => ref(0)
    </k>
    <env> 0 </env>
    <scopes>
      ( 0  |-> scope(.Map, parent(-1))
        -1 |-> builtinsScope )
      =>
      ( 0  |-> scope(
          "rescale_to_unit" |->
            closureVal(
              ("numbers", .ParamNames),
              Assign(
                Name("min_number"),
                Call(Name("min"), Name("numbers")))
              Assign(
                Name("max_number"),
                Call(Name("max"), Name("numbers")))
              Assign(Name("result"), ListExpr(.Exprs))
              Assign(
                Name("number"),
                Subscript(Name("numbers"), Int(0)))
              For(
                Name("number"),
                Name("numbers"),
                Expr(
                  Call(
                    Attribute(Name("result"), "append"),
                    BinOp(
                      "/",
                      BinOp("-", Name("number"), Name("min_number")),
                      BinOp("-", Name("max_number"), Name("min_number"))))))
              Return(Name("numbers")),
              0),
          parent(-1))
        -1 |-> builtinsScope )
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(
        scaleAcc(
          .ValSeq,
          vCons(FIRST,
            vCons(SECOND, REST)),
          minVF(vCons(FIRST,
            vCons(SECOND, REST))),
          maxVF(vCons(FIRST,
            vCons(SECOND, REST)))))
    </heap>
    <heapLoc> 0 => 1 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires
      allFloatVS(REST)
      andBool notBool eqF(
        minVF(vCons(FIRST, vCons(SECOND, REST))),
        maxVF(vCons(FIRST, vCons(SECOND, REST))))
endmodule
