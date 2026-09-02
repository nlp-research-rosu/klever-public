requires "verification.k"

module SPEC
  imports VERIFICATION

  claim [algebra-loop]:
    <k>
      #loop(
        zipObj(NUMBERS:ValSeq, OPERATIONS:ValSeq),
        TupleExpr(Name("oprn"), Name("oprt")),
        AugAssign(
          Name("expression"),
          "+",
          BinOp(
            "+",
            Call(Name("str"), Name("oprn")),
            Name("oprt"))))
      => .K
      ...
    </k>
    <env> 1 </env>
    <scopes>
      -1 |-> builtinsScope
      0 |-> scope("do_algebra" |-> FUNCTION:Val, parent(-1))
      1 |-> scope(
        "expression" |-> (
          str(ACC:IntSeq)
          =>
          str(runPairCodes(ACC, NUMBERS, OPERATIONS)))
        "oprn" |-> (OLDN:Val => lastPairValue(NUMBERS, OPERATIONS))
        "oprt" |-> (OLDO:Val => str(.IntSeq))
        "operator" |-> OPERATOR:Val
        "operand" |-> OPERAND:Val,
        parent(0))
    </scopes>
    requires validAlgebraLists(NUMBERS, OPERATIONS)

  claim [do-algebra]:
    <k>
      #loadAll(Module(
        FuncDef(
          "do_algebra",
          Params("operator", "operand"),
          Assign(Name("expression"), Str(""))
          Assign(Name("oprn"), Int(0))
          Assign(Name("oprt"), Str(""))
          For(
            TupleExpr(Name("oprn"), Name("oprt")),
            Call(
              Name("zip"),
              Name("operand"),
              BinOp("+", Name("operator"), ListExpr(Str("")))),
            AugAssign(
              Name("expression"),
              "+",
              BinOp(
                "+",
                Call(Name("str"), Name("oprn")),
                Name("oprt"))))
          Return(Call(Name("eval"), Name("expression"))))
        Assign(
          Name("answer"),
          Call(
            Name("do_algebra"),
            list(OPERATORS:ValSeq),
            list(OPERANDS:ValSeq)))))
      => .K
    </k>
    <env> 0 </env>
    <scopes>
      0 |-> scope(.Map, parent(-1))
      -1 |-> builtinsScope
      =>
      0 |-> scope(
        "answer" |->
          evalArith(
            runPairCodes(
              .IntSeq,
              OPERANDS,
              valSeqConcat(
                OPERATORS,
                vCons(str(.IntSeq), .ValSeq))))
        "do_algebra" |-> ?FUNCTION:Val,
        parent(-1))
      -1 |-> builtinsScope
    </scopes>
    <scopeLoc> 1 </scopeLoc>
    <heap>
      .Map
      =>
      0 |-> list(vCons(str(.IntSeq), .ValSeq))
      1 |-> list(
        valSeqConcat(
          OPERATORS,
          vCons(str(.IntSeq), .ValSeq)))
    </heap>
    <heapLoc> 0 => 2 </heapLoc>
    <stack> .List </stack>
    <ret> noRet </ret>
    <exc> NoExc </exc>
    <exit-code> 0 </exit-code>
    requires
      validAlgebraLists(
        OPERANDS,
        valSeqConcat(
          OPERATORS,
          vCons(str(.IntSeq), .ValSeq)))
      andBool notBool (OPERATORS ==K .ValSeq)
endmodule
